# Generates packs/pack-003.json — week 2: questions, be/do, Present Perfect vs Past Simple,
# phrasal verbs by particle logic (groups of 5), return of week-1 topics, harder listening.
# Run: python3 tools/content/gen3.py && python3 tools/validate_pack.py packs/pack-003.json
import json, math, hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from banks import R1, R2, R3, R4, R5, UX_ALT
from banks3 import Q1, Q2, BD, PP, NEAR, LISTEN, UX3, VOCAB3

ROOT = os.path.dirname(os.path.dirname(HERE))
BANK = {'Q1': Q1, 'Q2': Q2, 'BD': BD, 'PP': PP, 'R1': R1, 'R2': R2, 'R3': R3, 'R4': R4, 'R5': R5}
# lesson that explains each bank (the «Правило» button and the topic tag use it)
RULE = {'Q1': 'p3-d1-g1', 'Q2': 'p3-d2-g1', 'R3': 'p3-d3-g1', 'BD': 'p3-d4-g1', 'PP': 'p3-d5-g1',
        'R1': 'p2-d1-g1', 'R2': 'p2-d2-g1', 'R4': 'p2-d4-g1', 'R5': 'p2-d5-g1'}  # week-1 lessons (pack-002f) — short topic names for the tag
L_MEAN = 'Что означает эта фраза?'

def rnd(seed): return int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
def shuffle(lst, seed):
    a = list(lst); h = rnd(seed)
    for i in range(len(a) - 1, 0, -1):
        h = (h * 1103515245 + 12345) & 0xffffffff; j = h % (i + 1); a[i], a[j] = a[j], a[i]
    return a
def gap_of(en, ans):
    i = en.lower().find(ans.lower()); assert i >= 0, (en, ans)
    return en[:i] + '___' + en[i + len(ans):]

def row(b, k):
    r = BANK[b][2][k]
    return (r + (None,))[:8] if len(r) < 8 else r

def item(b, k, kind):
    en, ru, ans, dis, wrong, hint, alt, why = row(b, k)
    base = {'rule': RULE[b]}
    if why: base['why'] = why
    if kind == 'choice':
        opts = shuffle([ans] + dis, en)
        it = {'kind': 'choice', 'q': gap_of(en, ans), 'options': opts, 'a': opts.index(ans), 'explain': ru}
    elif kind == 'listen':
        near = NEAR[en]
        opts = shuffle([ru] + near, en + 'n')
        it = {'kind': 'choice', 'say': en, 'q': L_MEAN, 'options': opts, 'a': opts.index(ru), 'explain': en}
    elif kind == 'gap':
        it = {'kind': 'gap', 'q': gap_of(en, ans) + ' (' + hint + ')', 'a': [ans], 'explain': ru}
    elif kind == 'order':
        it = {'kind': 'order', 'en': en, 'ru': ru, 'alt': alt}
    elif kind == 'fix':
        assert wrong, (b, k)
        it = {'kind': 'fix', 'q': wrong, 'a': [en] + alt, 'explain': ru}
    elif kind == 'translate':
        it = {'kind': 'translate', 'ru': ru, 'a': [en] + alt}
    elif kind == 'shadow':
        it = {'kind': 'shadow', 'en': en, 'ru': ru}
    elif kind == 'dictation':
        it = {'kind': 'dictation', 'say': en, 'a': [en] + alt}
    else:
        raise ValueError(kind)
    it.update(base)
    return it

SEC = {'dictation': 30, 'choice': 9, 'listen': 10, 'gap': 20, 'order': 25, 'fix': 30, 'translate': 35, 'shadow': 15}
def minutes(items):
    return max(2, math.ceil(sum(SEC['listen' if (i['kind'] == 'choice' and 'say' in i) else i['kind']] for i in items) / 60))
def task(tid, ttype, title, items, **kw):
    t = {'id': tid, 'type': ttype, 'title': title, 'minutes': kw.pop('minutes', minutes(items)), 'items': items}
    t.update(kw); return t
def mixed(seed, specs):
    """specs: list of (bank, [rows], kind) → shuffled items (rows of different rules interleaved)"""
    out = [item(b, k, kind) for b, ks, kind in specs for k in ks]
    return shuffle(out, seed)

# ---------- phrasal verbs: particle logic ----------
PV = [  # verb, ru, example, example ru, particle sentence, particle, wrong particles, group
 ('find out', 'узнать (новое)', 'How did you find out about the job?', 'Как ты узнала об этой работе?', 'How did you find ___ about the job?', 'out', ['up', 'over'], 'out'),
 ('figure out', 'понять, разобраться самой', "I can't figure out what's wrong with the layout.", 'Не могу понять, что не так с макетом.', "I can't figure ___ what's wrong with the layout.", 'out', ['up', 'off'], 'out'),
 ('sort out', 'уладить, решить', "Don't worry, we'll sort it out.", 'Не переживай, мы с этим разберёмся.', "Don't worry, we'll sort it ___.", 'out', ['up', 'off'], 'out'),
 ('point out', 'указать, обратить внимание', 'She pointed out that the deadline was too tight.', 'Она обратила внимание, что дедлайн слишком сжатый.', 'She pointed ___ that the deadline was too tight.', 'out', ['up', 'over'], 'out'),
 ('run out of', 'закончиться (о запасе)', "We've run out of time.", 'У нас закончилось время.', "We've run ___ of time.", 'out', ['off', 'over'], 'out'),
 ('set up', 'организовать, настроить', 'Can you set up a call with the client?', 'Можешь организовать созвон с клиентом?', 'Can you set ___ a call with the client?', 'up', ['out', 'off'], 'up'),
 ('bring up', 'поднять тему', "Don't bring up salary in the first interview.", 'Не поднимай тему зарплаты на первом собеседовании.', "Don't bring ___ salary in the first interview.", 'up', ['out', 'over'], 'up'),
 ('come up with', 'придумать (идею)', 'She came up with a great idea.', 'Она придумала отличную идею.', 'She came ___ with a great idea.', 'up', ['out', 'on'], 'up'),
 ('give up', 'бросить, сдаться', "Don't give up, you're almost there.", 'Не сдавайся, ты почти у цели.', "Don't give ___, you're almost there.", 'up', ['out', 'off'], 'up'),
 ('catch up (on)', 'наверстать; обменяться новостями', 'I need to catch up on my emails.', 'Мне нужно разобрать накопившиеся письма.', 'I need to catch ___ on my emails.', 'up', ['out', 'over'], 'up'),
 ('call off', 'отменить', 'They called off the meeting.', 'Они отменили встречу.', 'They called ___ the meeting.', 'off', ['out', 'up'], 'off'),
 ('put off', 'отложить, перенести', "Let's put off the launch until March.", 'Давай отложим запуск до марта.', "Let's put ___ the launch until March.", 'off', ['out', 'on'], 'off'),
 ('go over', 'пройтись по, просмотреть', "Let's go over the feedback together.", 'Давай вместе пройдёмся по фидбэку.', "Let's go ___ the feedback together.", 'over', ['out', 'off'], 'over'),
 ('take over', 'взять на себя, принять дела', 'Who will take over the project when she leaves?', 'Кто возьмёт на себя проект, когда она уйдёт?', 'Who will take ___ the project when she leaves?', 'over', ['off', 'up'], 'over'),
 ('turn down', 'отклонить, отказаться', 'She turned down the job offer.', 'Она отклонила предложение о работе.', 'She turned ___ the job offer.', 'down', ['off', 'up'], 'other'),
 ('get back to', 'вернуться к кому-то с ответом', "I'll get back to you by Friday.", 'Я вернусь к вам с ответом до пятницы.', "I'll get ___ to you by Friday.", 'back', ['out', 'over'], 'other'),
 ('carry on', 'продолжать', 'Sorry, please carry on.', 'Извините, продолжайте.', 'Sorry, please carry ___.', 'on', ['off', 'out'], 'other'),
 ('look into', 'разобраться, изучить (проблему)', "I'll look into the problem tomorrow.", 'Я разберусь с проблемой завтра.', "I'll look ___ the problem tomorrow.", 'into', ['for', 'after'], 'other'),
 ('look forward to', 'ждать с нетерпением (+ -ing)', "I'm looking forward to working with you.", 'С нетерпением жду совместной работы.', "I'm looking forward ___ working with you.", 'to', ['for', 'at'], 'other'),
 ('fill in', 'заполнить (форму)', 'Please fill in this form.', 'Пожалуйста, заполните эту форму.', 'Please fill ___ this form.', 'in', ['up', 'out'], 'other'),
]
PV_NEAR = {
 'They called off the meeting.': ['Они отложили встречу.', 'Они назначили встречу.'],
 "Let's put off the launch until March.": ['Давай отменим запуск в марте.', 'Давай перенесём запуск на май.'],
 "I'll look into the problem tomorrow.": ['Я поищу проблему завтра.', 'Я разобралась с проблемой вчера.'],
 'She turned down the job offer.': ['Она приняла предложение о работе.', 'Она отклонила предложение о встрече.'],
 "I'll get back to you by Friday.": ['Я позвоню вам в пятницу.', 'Вы вернётесь ко мне с ответом до пятницы.'],
 'Who will take over the project when she leaves?': ['Кто возьмёт на себя проект, когда она вернётся?', 'Кто закончит проект, когда она уйдёт?'],
}
PV_VOCAB = {'find out': 'g26', 'figure out': 'g10', 'sort out': 'g29', 'point out': 'g11', 'run out of': 'g23',
            'set up': 'g19', 'bring up': 'g22', 'come up with': 'g9', 'give up': 'g27', 'catch up (on)': 'g32',
            'call off': 'g7', 'put off': 'g8', 'go over': 'g24', 'take over': 'g28', 'turn down': 'g20',
            'get back to': 'g25', 'carry on': 'g12', 'look into': 'g21', 'look forward to': 'g31', 'fill in': 'g30'}
GROUPS = {  # 5 verbs a day, by the logic of the particle
 1: ['find out', 'figure out', 'sort out', 'point out', 'run out of'],
 2: ['set up', 'bring up', 'come up with', 'give up', 'catch up (on)'],
 4: ['call off', 'put off', 'go over', 'take over', 'turn down'],
 5: ['get back to', 'carry on', 'look into', 'look forward to', 'fill in'],
}
PVI = {p[0]: p for p in PV}
PH_LES = 'p3-d3-g1'
def pv_particle(v, seed=''):
    verb, ru, ex, exru, q, part, wrong, g = PVI[v]
    opts = shuffle([part] + wrong, q + seed)
    return {'kind': 'choice', 'q': q, 'options': opts, 'a': opts.index(part), 'explain': f'{ex} — {exru}', 'rule': PH_LES, 'why': WHY_PART[part]}
def pv_meaning(v, k):
    verb, ru, ex, exru, q, part, wrong, g = PVI[v]
    others = [p for p in PV if p[0] != verb]
    same = [p for p in others if p[7] == g] + [p for p in others if p[7] != g]
    dis = shuffle(same[:4], verb)[:2]
    if k % 2 == 0:
        opts = shuffle([ru] + [d[1] for d in dis], verb + 'm')
        return {'kind': 'choice', 'q': f'**{verb}** — это…', 'options': opts, 'a': opts.index(ru), 'explain': f'{ex} — {exru}', 'rule': PH_LES}
    opts = shuffle([verb] + [d[0] for d in dis], verb + 'r')
    return {'kind': 'choice', 'q': f'«{ru}» — это…', 'options': opts, 'a': opts.index(verb), 'explain': f'{ex} — {exru}', 'rule': PH_LES}
WHY_PART = {
 'out': 'out = «наружу, до конца»: выяснить, решить, получить результат (find out, figure out, sort out, point out, run out of)',
 'up': 'up = «вверх, появиться, до конца»: set up, bring up, come up with, give up, catch up',
 'off': 'off = «прочь, отделить»: отменить или отодвинуть (call off, put off)',
 'over': 'over = «поверх, через»: просмотреть или перейти к себе (go over, take over)',
 'down': 'down = «вниз»: turn down — «опустить» предложение, отклонить',
 'back': 'back = «назад»: get back to someone — вернуться к человеку с ответом',
 'on': 'on = «дальше, продолжая»: carry on, go on',
 'into': 'into = «внутрь»: look into — заглянуть внутрь проблемы, разобраться',
 'to': 'look forward TO + -ing: to здесь предлог, поэтому working, а не work',
 'in': 'in = «внутрь»: fill in — вписать в поля формы',
}
def pv_block(day):
    vs = GROUPS[day]
    items = [pv_particle(v, f'd{day}') for v in vs] + [pv_meaning(v, k + day) for k, v in enumerate(vs)]
    return shuffle(items, f'pvb{day}')

# R3 rows by verb (week-1 bank) for gap/order/fix/translate on the phrasal day
def r3_rows():
    rows = R3[2]
    return list(range(len(rows)))

# ---------- lessons ----------
def lesson(lid, title, body, examples, minutes=5):
    return {'id': lid, 'type': 'lesson', 'title': title, 'minutes': minutes, 'body': body,
            'examples': [{'en': e, 'ru': r} for e, r in examples]}

LESSONS = {
 1: ('Вопросы: какой вспомогательный глагол', [
  'Схема английского вопроса всегда одна: **вспомогательный глагол + подлежащее + основной глагол**. Do you work…? Did she send…? Are you free?',
  'Как выбрать вспомогательный — посмотрите, что стоит после подлежащего:',
  '1) **Глагол действия** (work, like, need, send, understand) → **Do / Does / Did**. Сам глагол после них — в начальной форме: Did you **send** (не sent), Does she **use** (не uses).',
  '2) **Нет глагола действия** — только прилагательное, место, профессия (free, ready, sure, busy, happy, at home, a designer) → **be**: Are you free? Is it ready? Was it useful?',
  '3) **Уже есть -ing** → be: Are you working…? **Есть 3-я форма и важен результат** → have: Have you finished…? **Есть can / could / will / should** → они сами выходят вперёд: Can you share…?',
  'Логика: в утверждении вспомогательный «спрятан» (I work = I **do** work). В вопросе он просто выходит вперёд. Поэтому вопрос и отрицание строятся одинаково: **Do** you work? / I **don\'t** work.',
  'Быстрая проверка: если по-русски нельзя сказать «ты **делаешь** свободна» — значит, это be: Are you free?'],
  [('Do you work with developers every day?', 'Вы каждый день работаете с разработчиками?'), ('Does she use Figma at work?', 'Она пользуется Figma на работе?'),
   ('Are you free tomorrow?', 'Вы завтра свободны?'), ('Did you send the file yesterday?', 'Ты вчера отправила файл?'),
   ('Have you finished the mockups?', 'Ты закончила макеты?'), ('Are you working on the dashboard now?', 'Ты сейчас работаешь над дашбордом?'),
   ('Can everyone see my screen?', 'Всем видно мой экран?'), ('Are you sure about the colours?', 'Ты уверена насчёт цветов?')]),
 2: ('Вопросы: Wh-, к подлежащему, с предлогом, вежливые', [
  '**Wh-вопрос** = вопросительное слово + обычный вопрос из урока 1: Where **do you work**? What **did she say**? How long **have you been** here?',
  '**Вопрос к подлежащему — без do/did**, порядок как в утверждении: **Who called** you? **What happened**? **Which option works** better? Логика: вопросительное слово само стало подлежащим — переставлять нечего.',
  'Сравните: **Who called you?** — Кто тебе звонил? (неизвестно, КТО звонил) · **Who did you call?** — Кому ты звонила? (неизвестно, КОМУ)',
  '**Предлог уходит в конец**: What are you working **on**? Who did you talk **to**? What is this **for**? По-русски он впереди («над чем», «с кем», «для чего») — в английском в конце.',
  '**Вежливый вопрос** (Could you tell me… / Do you know… / I wonder…) — дальше **прямой порядок, без do**: Could you tell me **where the file is**? Do you know **when the meeting starts**? Логика: вопрос уже задан первой частью — второй раз переставлять не нужно.'],
  [('Where do you work?', 'Где ты работаешь?'), ('Who called you?', 'Кто тебе звонил?'), ('Who did you call?', 'Кому ты звонила?'),
   ('What happened?', 'Что случилось?'), ('What are you working on?', 'Над чем ты работаешь?'), ('Who is this screen for?', 'Для кого этот экран?'),
   ('Could you tell me where the file is?', 'Не подскажете, где файл?'), ('Do you know when the meeting starts?', 'Ты не знаешь, когда начинается встреча?')]),
 3: ('Фразовые глаголы: логика частиц', [
  'Частица — не случайная: у каждой есть «картинка». Если видеть картинку, глагол запоминается без зубрёжки.',
  '**OUT — «наружу, до конца»**: достать результат. find out (узнать), figure out (понять самой), sort out (уладить), point out (указать), run out of (закончиться — запас «вышел»).',
  '**UP — «вверх, появиться, до конца»**: set up (организовать — «поставить»), bring up (поднять тему), come up with (придумать — идея «всплыла»), give up (бросить), catch up (on) (догнать, наверстать).',
  '**OFF — «прочь, отделить»**: call off (отменить — «отозвать»), put off (отложить — «отодвинуть»).',
  '**OVER — «поверх, через»**: go over (пройтись поверх — просмотреть), take over (взять себе — принять дела).',
  '**Остальные**: turn **down** (опустить — отклонить), get **back** to (вернуться к человеку с ответом), carry **on** (дальше — продолжать), look **into** (заглянуть внутрь — разобраться), fill **in** (вписать — заполнить), look forward **to** + -ing (ждать с нетерпением).',
  'С местоимением частица встаёт после него: **sort it out**, call **it** off. Ниже — все 20 глаголов с примерами, нажмите ▶ и повторите вслух.'],
  [(f'{p[0]} — {p[2]}', f'{p[1]} — {p[3]}') for p in PV]),
 4: ('be или do: am / is / are или do / does', [
  'Главное правило недели: **be** — когда после подлежащего нет глагола действия (прилагательное, место, -ing). **do** — когда глагол действия есть.',
  'Отрицание: **be + not** — I\'m not sure, It isn\'t visible, We aren\'t ready. **do + not + глагол** — I don\'t understand, It doesn\'t make sense, She doesn\'t like…',
  'Ловушка для русскоязычных: sure, afraid, ready, busy, happy, interested, confident — по-русски это «уверена», «боюсь», «готова», а в английском — прилагательные. Поэтому **I\'m not sure**, **Don\'t be afraid**, **I\'m interested in**.',
  '**Present Simple** (I work, she works) — обычно, регулярно (usually, every day, on Fridays). **Present Continuous** (I\'m working) — прямо сейчас или в этот период (now, this week, still).',
  '**-ing никогда не стоит один**: I**\'m** working, she**\'s** waiting, we**\'re** testing. «I still working» — ошибка: нужен am.',
  'Глаголы восприятия и состояния обычно без -ing: it **sounds**, it **looks**, I **know**, I **like**, I **need**, it **doesn\'t make** sense.'],
  [("I'm not sure about this colour.", 'Я не уверена насчёт этого цвета.'), ("It doesn't make sense.", 'Это не имеет смысла.'),
   ("Don't be afraid to ask.", 'Не бойся спрашивать.'), ("I'm still working on the empty states.", 'Я всё ещё работаю над пустыми состояниями.'),
   ('We usually test with five users.', 'Обычно мы тестируем на пяти пользователях.'), ("We're testing the new flow this week.", 'На этой неделе мы тестируем новый сценарий.'),
   ("It doesn't sound very difficult.", 'Звучит не очень сложно.'), ("I'm interested in reading the analysis.", 'Мне интересно читать разбор.')]),
 5: ('Present Perfect или Past Simple', [
  '**Past Simple** (worked, launched, did) — важно КОГДА. Событие закончилось, и время названо или понятно: yesterday, last week, in May, two years ago, at my previous job, When…?',
  '**Present Perfect** (have / has + 3-я форма) — важен РЕЗУЛЬТАТ СЕЙЧАС, а время не важно или ещё идёт: just, already, yet, ever, never, today, this week, since, for (до сих пор).',
  'Логика: **have** = «имею сейчас». I **have** finished = у меня сейчас есть готовый результат. Поэтому с yesterday нельзя: вчера — это не «сейчас».',
  '**Сколько уже — и до сих пор**: I\'**ve been** a designer **for** three years / **since** 2022. А «работала два года, но больше нет»: I **worked** there for two years.',
  'Рабочие отчёты: что сделали на встрече или тесте → обычно Past Simple (we checked, users said). Цифры на сегодня → Present Perfect (conversion **has increased**).',
  'Самые нужные 3-и формы: been, done, made, seen, sent, told, taken, gone, had, lost, left, met, found, fixed, finished.'],
  [("I've been a designer for three years.", 'Я работаю дизайнером три года.'), ('We launched the app in May.', 'Мы запустили приложение в мае.'),
   ("I've just sent you the link.", 'Я только что отправила тебе ссылку.'), ("I haven't finished the report yet.", 'Я ещё не закончила отчёт.'),
   ('Conversion has increased by 12%.', 'Конверсия выросла на 12%.'), ('We checked the layouts yesterday.', 'Вчера мы проверили макеты.'),
   ('I worked there for two years.', 'Я проработала там два года (больше не работаю).'), ("I've worked here for two years.", 'Я работаю здесь два года (и сейчас).')]),
 6: ('Неделя 1: возвращаемся с логикой', [
  '**make или do.** make — СОЗДАЁМ, появляется результат: make a plan, a copy, coffee, a decision, a call, progress, money, an effort, a suggestion, changes, a mistake. do — ВЫПОЛНЯЕМ работу, действие: do homework, the cleaning, business, damage, a favour, your best, exercise, good (Exercise does you good).',
  '**used to — три формы, три смысла.** used to + глагол = «раньше (а теперь нет)»: I used to work in an office · There used to be a café here. be used to + -ing = «привыкла (это нормально)»: I\'m used to working remotely. get used to + -ing = «привыкаю / привыкну»: She\'s getting used to the new tool.',
  'Проверка для used to: можно сказать «к этому»? (привыкла к этому) → be/get used to + -ing. «Раньше…» → used to + глагол. В вопросе и отрицании «раньше»: Did you use to…? / didn\'t use to (без d).',
  '**wish.** О настоящем — шаг назад: I wish I **had** more time / **could** speak. О прошлом — had + 3-я форма: I wish I **hadn\'t said** it · They wish they **hadn\'t sold** the house. Хочу, чтобы другой изменился — would: I wish you **would** stop.',
  '**Двойники.** compelling — убедительный · compulsory — обязательный · sensible — разумный · sensitive — чувствительный · affect (глагол, без on) · an effect on (существительное) · advice (совет) · advise (советовать) · lose (терять) · loose (свободный).'],
  [('We need to make a decision today.', 'Нам нужно принять решение сегодня.'), ('The storm did a lot of damage.', 'Буря нанесла большой ущерб.'),
   ('There used to be a café on this corner.', 'Раньше на этом углу было кафе.'), ("I'm used to working remotely.", 'Я привыкла работать удалённо.'),
   ("They wish they hadn't sold the house.", 'Они жалеют, что продали дом.'), ('These trousers are too loose.', 'Эти брюки слишком свободные.')], 6),
}

WRITES = {
 1: ('Своя речь: вопросы пользователю', 'Вы готовите интервью с пользователями приложения доставки еды. Напишите 6 вопросов: 2 с **do/does**, 2 с **did**, 1 с **be** (is/are/was), 1 с **have** (Have you ever…?).', 'Например: How often do you order food? Did you have any problems last time? Is it easy to find…?', 30),
 2: ('Своя речь: уточняющие вопросы', 'Напишите разработчику в Slack 4–5 уточняющих вопросов по новой задаче: 2 прямых (What…? When…? Who…?), 2 вежливых (Could you tell me… / Do you know…) и 1 с предлогом в конце (What is it for? Who should I talk to?).', 'Помните: в вежливом вопросе — прямой порядок: Could you tell me when the release is?', 35),
 3: ('Своя речь: история с фразовыми', 'Расскажите о рабочей ситуации, когда что-то пошло не так и вы это решили. Используйте 5 фразовых глаголов из урока (например: call off, put off, figure out, sort out, get back to).', 'Можно начать: Last month we had to call off… / It took me a day to figure out…', 50),
 4: ('Своя речь: обычно и сейчас', 'Напишите о себе: что вы **обычно** делаете на работе (I work, I usually…), чем заняты **на этой неделе** (I\'m working on…, we\'re testing…) и чего **не** делаете (I don\'t…, I\'m not…). Минимум 3 отрицания: с don\'t/doesn\'t и с am not / isn\'t.', 'Подсказка: I\'m not sure… / It doesn\'t… / I\'m interested in…', 50),
 5: ('Своя речь: мой проект в цифрах', 'Расскажите о проекте: что вы сделали и **когда** (we launched… in…, last year we…), какой результат **сейчас** (it has increased…, we have reduced…), и как давно вы в профессии (I\'ve been… for…).', 'Если цифр нет — придумайте правдоподобные.', 60),
 6: ('Своя речь: неделя 1 возвращается', 'Напишите о переменах в вашей жизни: что раньше было иначе (used to), к чему вы привыкли или привыкаете (be / get used to + -ing), о чём жалеете (wish + had done / could). Используйте make и do минимум по 2 раза.', 'Например: I used to… / I\'m getting used to… / I wish I had… / It made a big difference…', 60),
 7: ('Своя речь: итоги недели 2', 'Что за эту неделю далось легко, что трудно, что хотите повторить? В конце задайте 2 вопроса — себе или мне (по правилам недели).', 'Например: What should I review first? / Did I use the Present Perfect correctly?', 50),
}

# ---------- build ----------
days = []
def gid(d, n): return f'p3-d{d}-g{n}'
def uid(d, n): return f'p3-d{d}-u{n}'
RULEBANK = {1: 'Q1', 2: 'Q2', 4: 'BD', 5: 'PP'}
W1 = [('R1', 'make/do'), ('R2', 'used to'), ('R4', 'wish'), ('R5', 'pairs')]

for d in range(1, 8):
    day = {'day': d, 'general': [], 'ux': []}
    G, U = day['general'], day['ux']
    if d in RULEBANK:
        b = RULEBANK[d]
        title, body, ex = LESSONS[d][:3]
        day['title'] = {1: 'Вопросы: вспомогательный глагол', 2: 'Вопросы: Wh-, кто?, предлог, вежливые', 4: 'be или do', 5: 'Present Perfect / Past Simple'}[d]
        G.append(lesson(gid(d, 1), title, body, ex))
        G.append(task(gid(d, 2), 'mix', 'Узнавание: выберите вариант', [item(b, k, 'choice') for k in range(0, 10)]))
        G.append(task(gid(d, 3), 'mix', 'Понимание на слух', [item(b, k, 'listen') for k in LISTEN[b]]))
        G.append(task(gid(d, 4), 'gap', 'Впишите нужную форму', [item(b, k, 'gap') for k in range(10, 20)]))
        G.append(task(gid(d, 5), 'order', 'Соберите предложение', [item(b, k, 'order') for k in range(20, 26)]))
        G.append(task(gid(d, 6), 'fix', 'Найдите и исправьте ошибку', [item(b, k, 'fix') for k in range(26, 32)]))
        G.append(task(gid(d, 7), 'translate', 'Переведите на английский', [item(b, k, 'translate') for k in [0, 1, 2, 3, 10, 11, 12, 13, 32, 33]]))
        G.append(task(gid(d, 8), 'shadow', 'Повторите вслух (shadowing)', [item(b, k, 'shadow') for k in range(32, 40)]))
        G.append(task(gid(d, 9), 'mix', 'Фразовые: 5 на сегодня', pv_block(d)))
        # review: earlier rules of this week + week-1 topics, interleaved
        prev = [x for x in ('Q1', 'Q2', 'BD') if x in [RULEBANK[k] for k in RULEBANK if k < d]]
        specs = []
        for i, pb in enumerate(prev):
            specs += [(pb, [34 + i, 35 + i], 'choice'), (pb, [16 + i], 'gap'), (pb, [4 + i], 'translate')]
        w1 = {1: [('R1', [10, 11, 12], 'choice'), ('R1', [20], 'translate'), ('R2', [12, 13], 'choice'), ('R2', [22], 'gap'), ('R4', [10], 'choice'), ('R4', [21], 'translate'), ('R5', [11, 12], 'choice'), ('R5', [21], 'translate')],
              2: [('R1', [13, 14], 'choice'), ('R1', [21], 'gap'), ('R2', [14], 'choice'), ('R2', [23], 'translate'), ('R4', [11], 'gap'), ('R5', [13], 'choice')],
              4: [('R1', [15], 'choice'), ('R1', [22], 'translate'), ('R2', [15], 'choice'), ('R2', [24], 'gap'), ('R4', [12], 'choice'), ('R5', [14], 'choice')],
              5: [('R1', [16], 'choice'), ('R1', [23], 'gap'), ('R2', [16], 'choice'), ('R4', [13], 'translate'), ('R5', [15], 'choice')]}[d]
        G.append(task(gid(d, 10), 'mix', 'Повторение: прошлые дни и неделя 1', mixed(f'rev{d}', specs + w1)))
        w = WRITES[d]
        G.append({'id': gid(d, 11), 'type': 'write', 'title': w[0], 'minutes': 7, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})
    elif d == 3:
        day['title'] = 'Фразовые глаголы: логика частиц'
        title, body, ex = LESSONS[3][:3]
        G.append(lesson(gid(3, 1), title, body, ex, 8))
        G.append(task(gid(3, 2), 'mix', 'Какая частица? (out / up / off / over…)', shuffle([pv_particle(p[0]) for p in PV], 'part3')))
        G.append(task(gid(3, 3), 'mix', 'Квиз: глагол ↔ значение', shuffle([pv_meaning(p[0], k) for k, p in enumerate(PV)], 'quiz3')))
        lis = []
        for en, near in PV_NEAR.items():
            p = next(x for x in PV if x[2] == en)
            opts = shuffle([p[3]] + near, en + 'n')
            lis.append({'kind': 'choice', 'say': en, 'q': L_MEAN, 'options': opts, 'a': opts.index(p[3]), 'explain': en, 'rule': PH_LES})
        G.append(task(gid(3, 4), 'mix', 'Понимание на слух', lis))
        G.append(task(gid(3, 5), 'gap', 'Впишите глагол (подсказка по-русски)', [item('R3', k, 'gap') for k in range(0, 10)]))
        G.append(task(gid(3, 6), 'order', 'Соберите предложение', [item('R3', k, 'order') for k in range(10, 16)]))
        fixrows = [k for k in range(32, 40) if R3[2][k][4]][:6]
        G.append(task(gid(3, 7), 'fix', 'Найдите и исправьте ошибку', [item('R3', k, 'fix') for k in fixrows]))
        G.append(task(gid(3, 8), 'translate', 'Переведите на английский', [item('R3', k, 'translate') for k in range(20, 30)]))
        G.append(task(gid(3, 9), 'shadow', 'Повторите вслух (shadowing)', [{'kind': 'shadow', 'en': p[2], 'ru': p[3], 'rule': PH_LES} for p in PV[::2]]))
        specs = [('Q1', [30, 31, 33], 'choice'), ('Q1', [17], 'gap'), ('Q1', [8], 'translate'), ('Q2', [30, 32, 33], 'choice'), ('Q2', [18], 'gap'), ('Q2', [9], 'translate'), ('R1', [17], 'choice'), ('R2', [17], 'choice')]
        G.append(task(gid(3, 10), 'mix', 'Повторение: вопросы и неделя 1', mixed('rev3', specs)))
        w = WRITES[3]
        G.append({'id': gid(3, 11), 'type': 'write', 'title': w[0], 'minutes': 8, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})
    elif d == 6:
        day['title'] = 'Неделя 1 возвращается'
        title, body, ex, mins = LESSONS[6]
        G.append(lesson(gid(6, 1), title, body, ex, mins))
        G.append(task(gid(6, 2), 'mix', 'make или do', mixed('md6', [('R1', [24, 25, 26, 27, 28, 29], 'choice'), ('R1', [30, 31, 32, 33], 'gap')])))
        G.append(task(gid(6, 3), 'mix', 'used to / be used to / get used to', mixed('ut6', [('R2', [25, 26, 27, 28], 'choice'), ('R2', [29, 30, 31, 32], 'gap'), ('R2', [33, 34], 'translate')])))
        G.append(task(gid(6, 4), 'mix', 'Слова-двойники', mixed('pr6', [('R5', [24, 25, 26, 27, 28, 29], 'choice'), ('R5', [30, 31], 'translate')])))
        G.append(task(gid(6, 5), 'mix', 'wish и if only', mixed('ws6', [('R4', [24, 25, 26], 'choice'), ('R4', [27, 28], 'gap'), ('R4', [29, 30, 31], 'translate')])))
        dict_items = [item(b, k, 'dictation') for b, k in [('Q1', 23), ('Q2', 26), ('BD', 9), ('PP', 4), ('Q2', 34), ('BD', 23), ('PP', 17), ('Q1', 36)]]
        G.append(task(gid(6, 6), 'dictation', 'Диктант: вопросы и времена', dict_items, minutes=5))
        G.append(task(gid(6, 7), 'mix', 'Фразовые: все 20 (повторение)', shuffle([pv_meaning(p[0], k + 1) for k, p in enumerate(PV[::2])] + [pv_particle(p[0], 'd6') for p in PV[1::2]], 'pv6')))
        w = WRITES[6]
        G.append({'id': gid(6, 8), 'type': 'write', 'title': w[0], 'minutes': 8, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})
    else:
        day['title'] = 'Итог недели 2'
        specs = [('Q1', [36, 37, 38], 'choice'), ('Q1', [18], 'gap'), ('Q2', [35, 36, 37], 'choice'), ('Q2', [19], 'gap'),
                 ('BD', [34, 35, 36], 'choice'), ('BD', [16, 17], 'gap'), ('PP', [34, 35, 36], 'choice'), ('PP', [16, 17], 'gap')]
        G.append(task(gid(7, 1), 'mix', 'Итоговая практика: вопросы, be/do, времена', mixed('fin7', specs)))
        G.append(task(gid(7, 2), 'mix', 'Итог: фразовые глаголы', shuffle([pv_particle(p[0], 'd7') for p in PV[::2]] + [pv_meaning(p[0], k) for k, p in enumerate(PV[1::2])], 'pv7')))
        G.append(task(gid(7, 3), 'translate', 'Итоговый перевод', mixed('tr7', [('Q1', [9, 21], 'translate'), ('Q2', [14, 21], 'translate'), ('BD', [24, 37], 'translate'), ('PP', [5, 21], 'translate'), ('R1', [34], 'translate'), ('R2', [35], 'translate'), ('R4', [32], 'translate'), ('R5', [32], 'translate')])))
        G.append(task(gid(7, 4), 'shadow', 'Итог: повторите вслух', [item(b, k, 'shadow') for b, k in [('Q1', 37), ('Q2', 7), ('BD', 0), ('BD', 3), ('PP', 0), ('PP', 7), ('Q2', 10), ('BD', 9)]]))
        w = WRITES[7]
        G.append({'id': gid(7, 5), 'type': 'write', 'title': w[0], 'minutes': 8, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})

    # ---------- UX ----------
    def ux_alt(e): return [e] + [x for x in UX_ALT.get(e, []) if x != e]
    def ux_listen(ph, seed):
        out = []
        for e, r, near in ph:
            if not near: continue
            opts = shuffle([r] + near, e + seed)
            out.append({'kind': 'choice', 'say': e, 'q': L_MEAN, 'options': opts, 'a': opts.index(r), 'explain': e})
        return out
    if d <= 6:
        th, ph = UX3[d - 1]
        U.append({'id': uid(d, 1), 'type': 'lesson', 'title': 'Фразы: ' + th[0].lower() + th[1:], 'minutes': 4,
                  'body': ['16 рабочих фраз. Прослушайте каждую (▶) и повторите вслух — потом они встретятся в упражнениях.'] +
                          (['Это фразы, которые на прошлой неделе не вспоминались в нужный момент. Сегодня — только они, чтобы закрепить.'] if d == 6 else []),
                  'examples': [{'en': e, 'ru': r} for e, r, _ in ph]})
        U.append(task(uid(d, 2), 'mix', 'Понимание на слух', ux_listen(ph, f'u{d}')))
        U.append(task(uid(d, 3), 'translate', 'Переведите на английский', [{'kind': 'translate', 'ru': r, 'a': ux_alt(e)} for e, r, _ in ph[0:8]]))
        U.append(task(uid(d, 4), 'order', 'Соберите фразу', [{'kind': 'order', 'en': e, 'ru': r, 'alt': UX_ALT.get(e, [])} for e, r, _ in ph[8:14]]))
        U.append(task(uid(d, 5), 'shadow', 'Повторите вслух', [{'kind': 'shadow', 'en': e, 'ru': r} for e, r, _ in ph[0:16:2]]))
        n = 6
        cards = {3: ['u13', 'u14', 'u15', 'u16', 'u17'], 4: ['u18', 'u19', 'u20', 'u21'], 5: ['u22', 'u23', 'u24']}.get(d)
        if cards:
            U.append({'id': uid(d, n), 'type': 'cards', 'title': 'Слова для работы', 'minutes': 3, 'cards': cards}); n += 1
        if d == 3:
            U.append({'id': uid(d, n), 'type': 'write', 'title': 'Итоги юзабилити-теста в Slack', 'minutes': 7,
                      'prompt': 'Напишите команде в Slack итоги теста: сколько было участников, 3 главные находки (что пошло не так и где пользователи застряли) и что предлагаете дальше.',
                      'hint': 'Пригодится: participants, got stuck, didn\'t notice, key finding, it might be worth…, I\'ll share the recordings.', 'minWords': 50}); n += 1
        if d == 5:
            U.append({'id': uid(d, n), 'type': 'write', 'title': 'Отчёт о результатах для клиента', 'minutes': 8,
                      'prompt': 'Напишите клиенту короткий отчёт после редизайна: что и когда запустили (Past Simple), что изменилось в цифрах (Present Perfect: has increased, have fallen), что пока рано оценивать и что предлагаете дальше.',
                      'hint': 'We launched… in… / Since then, … has… / We haven\'t seen… yet / It\'s too early to… / I\'d suggest…', 'minWords': 60}); n += 1
        # spaced review of earlier phrases (week-1 hard phrases start on day 1)
        hard = UX3[5][1]
        rev = {1: hard[0:6], 2: UX3[0][1][0:4] + hard[6:10], 3: UX3[1][1][0:4] + hard[10:14], 4: UX3[2][1][4:8] + hard[0:4],
               5: UX3[3][1][0:4] + hard[4:8], 6: UX3[4][1][0:4] + UX3[0][1][8:12]}[d]
        U.append(task(uid(d, n), 'translate', 'Повторение фраз прошлых дней', [{'kind': 'translate', 'ru': r, 'a': ux_alt(e)} for e, r, _ in rev]))
    else:
        allp = [x for i in range(5) for x in UX3[i][1]]
        pk = shuffle(allp, 'ux7-3')
        U.append(task(uid(7, 1), 'translate', 'Итог: рабочие фразы', [{'kind': 'translate', 'ru': r, 'a': ux_alt(e)} for e, r, _ in pk[:12]]))
        U.append(task(uid(7, 2), 'order', 'Итог: соберите фразы', [{'kind': 'order', 'en': e, 'ru': r} for e, r, _ in pk[12:20]]))
        U.append(task(uid(7, 3), 'mix', 'Итог: понимание на слух', shuffle(ux_listen([x for x in allp if x[2]], 'u7'), 'u7l')[:8]))
        U.append(task(uid(7, 4), 'shadow', 'Итог: повторите вслух', [{'kind': 'shadow', 'en': e, 'ru': r} for e, r, _ in pk[20:28]]))
    days.append(day)

vocab = [{'id': i, 'en': en, 'ru': ru, 'ex': ex, 'lvl': lvl, 'tag': tag} for i, en, ru, ex, lvl, tag in VOCAB3]
pack = {
 'type': 'study-pack', 'version': 1, 'id': 'pack-003', 'title': 'Неделя 2: строим фразы — вопросы, be/do, времена',
 'level': 'B1', 'created': '2026-11-14',
 'method': 'Каждое правило — с логикой «почему так»; этапы навыка (правило → контролируемая практика → своя речь); интервальное повторение (правила недели 1 возвращаются каждый день); фразовые глаголы — по логике частиц, по 5 в день; на слух — варианты отличаются одной деталью.',
 'vocab': vocab, 'days': days,
}
json.dump(pack, open(os.path.join(ROOT, 'packs', 'pack-003.json'), 'w'), ensure_ascii=False, indent=1)
n = sum(len(t.get('items', [])) for d in days for s in ('general', 'ux') for t in d[s])
print('pack-003:', len(days), 'days,', sum(len(d['general']) + len(d['ux']) for d in days), 'tasks,', n, 'items')
for d in days:
    print(d['day'], d['title'], '·', sum(t.get('minutes', 0) for t in d['general']), '+', sum(t.get('minutes', 0) for t in d['ux']), 'min')
