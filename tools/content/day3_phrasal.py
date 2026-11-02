# Rebuilds pack-002 day 3 in the new phrasal-verb format (user decision 02.11.2026):
# list lesson (verb · translation · example) -> cards -> quiz -> the usual exercises.
import json, random, copy
ROOT = '/home/claude/study'
p = json.load(open(ROOT + '/packs/pack-002.json'))

VERBS = [  # (vocab id, verb, translation, example en, example ru)
 ('g7',  'call off', 'отменить', 'They called off the meeting.', 'Они отменили встречу.'),
 ('g8',  'put off', 'откладывать, переносить', "Let's put off the launch until March.", 'Давай отложим запуск до марта.'),
 ('g9',  'come up with', 'придумать, предложить (идею)', 'She came up with a great idea.', 'Она придумала отличную идею.'),
 ('g10', 'figure out', 'разобраться, понять самой', "I can't figure out what's wrong with the layout.", 'Не могу понять, что не так с макетом.'),
 ('g11', 'point out', 'указать (другим), обратить внимание', 'She pointed out that the deadline was too tight.', 'Она обратила внимание, что дедлайн слишком сжатый.'),
 ('g12', 'carry on', 'продолжать', 'Sorry, please carry on.', 'Извините, продолжайте.'),
 ('g19', 'set up', 'организовать, настроить', 'Can you set up a call with the client?', 'Можешь организовать созвон с клиентом?'),
 ('g20', 'turn down', 'отклонить, отказаться', 'She turned down the job offer.', 'Она отклонила предложение о работе.'),
 ('g21', 'look into', 'разобраться, изучить (проблему)', "I'll look into the problem tomorrow.", 'Я разберусь с проблемой завтра.'),
 ('g22', 'bring up', 'поднять тему, упомянуть', "Don't bring up salary in the first interview.", 'Не поднимай тему зарплаты на первом собеседовании.'),
 ('g23', 'run out of', 'закончиться (о запасе)', "We've run out of time.", 'У нас закончилось время.'),
 ('g24', 'go over', 'пройтись по, просмотреть', "Let's go over the feedback together.", 'Давай вместе пройдёмся по фидбэку.'),
 ('g25', 'get back to', 'вернуться к кому-то с ответом', "I'll get back to you by Friday.", 'Я вернусь к вам с ответом до пятницы.'),
 ('g26', 'find out', 'узнать (новую информацию)', 'How did you find out about the job?', 'Как ты узнала об этой работе?'),
 ('g27', 'give up', 'сдаться, бросить', "Don't give up, you're almost there.", 'Не сдавайся, ты почти у цели.'),
 ('g28', 'take over', 'взять на себя, принять дела', 'Who will take over the project when she leaves?', 'Кто возьмёт на себя проект, когда она уйдёт?'),
 ('g29', 'sort out', 'решить, уладить', "Don't worry, we'll sort it out.", 'Не переживай, мы с этим разберёмся.'),
 ('g30', 'fill in', 'заполнить (форму)', 'Please fill in this form.', 'Пожалуйста, заполните эту форму.'),
 ('g31', 'look forward to', 'ждать с нетерпением (+ -ing)', "I'm looking forward to working with you.", 'С нетерпением жду совместной работы.'),
 ('g32', 'catch up (on)', 'наверстать; обменяться новостями', 'I need to catch up on my emails.', 'Мне нужно разобрать накопившиеся письма.'),
]
# confusable pairs for the quiz: wrong options from the same "family" first
FAMILY = {'look into': ['look for', 'look after'], 'carry on': ['carry out', 'go off'], 'point out': ['figure out', 'find out'],
          'figure out': ['point out', 'find out'], 'find out': ['figure out', 'look into'], 'turn down': ['turn off', 'call off'],
          'call off': ['put off', 'turn down'], 'put off': ['call off', 'put on'], 'set up': ['sort out', 'take over'],
          'take over': ['take off', 'set up'], 'give up': ['give in', 'put off'], 'go over': ['go off', 'look into'],
          'get back to': ['get over', 'look forward to'], 'bring up': ['come up with', 'point out'], 'come up with': ['bring up', 'figure out'],
          'run out of': ['give up', 'run over'], 'sort out': ['set up', 'figure out'], 'fill in': ['fill up', 'set up'],
          'look forward to': ['look into', 'get back to'], 'catch up (on)': ['carry on', 'go over']}
TR = {v[1]: v[2] for v in VERBS}
def opts(right, wrong, seed):
    o = [right] + wrong[:2]; r = random.Random(seed); r.shuffle(o); return o, o.index(right)

vocab_new = [{"id": i, "en": en, "ru": ru, "ex": ex, "lvl": "B2" if en not in ('fill in', 'find out', 'give up', 'set up') else "B1", "tag": "general"}
             for i, en, ru, ex, _ in VERBS if i not in {v['id'] for v in p['vocab']}]

LES = 'p2-d3-n1'
lesson = {"id": LES, "type": "lesson", "title": "Фразовые глаголы дня: список", "minutes": 6,
  "body": ["20 глаголов этого дня. Прочитайте каждый вслух вместе с примером и нажмите ▶, чтобы услышать произношение.",
           "Учите глагол целиком, вместе с частицей: частица меняет смысл — **look for** «искать», а **look into** «разобраться»."],
  "examples": [{"en": f"{en} — {ex}", "ru": f"{ru} — {exru}"} for _, en, ru, ex, exru in VERBS]}
cards = {"id": "p2-d3-n2", "type": "cards", "title": "Карточки: все 20 глаголов", "minutes": 6, "cards": [v[0] for v in VERBS]}
quiz_items = []
for k, (_, en, ru, ex, exru) in enumerate(VERBS):
    if k % 2 == 0:   # verb -> meaning
        wrong = [TR[w] for w in FAMILY[en] if w in TR] + [TR[v[1]] for v in VERBS if v[1] not in (en, *FAMILY[en])]
        o, a = opts(ru, wrong, k)
        quiz_items.append({"kind": "choice", "q": f"**{en}** — это…", "options": o, "a": a, "explain": f"{ex} — {exru}", "rule": LES})
    else:            # meaning -> verb
        o, a = opts(en, FAMILY[en], k)
        quiz_items.append({"kind": "choice", "q": f"«{ru}» — это…", "options": o, "a": a, "explain": f"{ex} — {exru}", "rule": LES})
quiz = {"id": "p2-d3-n3", "type": "mix", "title": "Квиз: 20 глаголов", "minutes": 5, "items": quiz_items}

d = p['days'][2]
old = {t['id']: t for t in d['general']}
rest = []
for k, oid in enumerate(['p2-d3-g2', 'p2-d3-g3', 'p2-d3-g4', 'p2-d3-g5', 'p2-d3-g6', 'p2-d3-g7', 'p2-d3-g8', 'p2-d3-g9', 'p2-d3-g11'], start=4):
    t = copy.deepcopy(old[oid]); t['id'] = f'p2-d3-n{k}'
    for it in t.get('items', []):
        if oid != 'p2-d3-g9': it['rule'] = LES
    # 01.11: ambiguous choice (figured out / pointed out) — replace the distractor
    for it in t.get('items', []):
        if it.get('kind') == 'choice' and 'mistake in the flow' in it.get('q', '') and 'figured out' in it.get('options', []):
            it['options'] = [x if x != 'figured out' else 'looked into' for x in it['options']]
    if oid == 'p2-d3-g11': t['hint'] = 'set up, look into, come up with, put off, get back to… Минимум — рекомендация.'
    rest.append(t)
d['general'] = [lesson, cards, quiz] + rest
d['title'] = 'Фразовые глаголы для работы'

p['id'] = 'pack-002b'; p['replaces'] = ['pack-002']; p['updated'] = '2026-11-02'
p['title'] = p['title'].replace('Неделя 1 · плотная', 'Неделя 1 · плотная (д3 — новый формат)') if 'Неделя 1 · плотная' in p['title'] else p['title']
p['vocab'] = p['vocab'] + vocab_new
json.dump(p, open(ROOT + '/packs/pack-002b.json', 'w'), ensure_ascii=False, indent=1)
print(p['title'], len(vocab_new), [t['id'] + ':' + t['type'] for t in d['general']])
