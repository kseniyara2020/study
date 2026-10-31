import json, math, hashlib, sys
sys.path.insert(0, '/home/claude/content')
from banks import R1, R2, R3, R4, R5, UX

OLD = json.load(open('/home/claude/pack-001.json'))
oldt = {t['id']: t for d in OLD['days'] for s in ('general', 'ux') for t in d[s]}
RULES = [R1, R2, R3, R4, R5]

def rnd(seed):
    return int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)

def shuffle(lst, seed):
    a = list(lst)
    h = rnd(seed)
    for i in range(len(a) - 1, 0, -1):
        h = (h * 1103515245 + 12345) & 0xffffffff
        j = h % (i + 1)
        a[i], a[j] = a[j], a[i]
    return a

def gap_of(en, ans):
    i = en.lower().find(ans.lower())
    assert i >= 0, (en, ans)
    return en[:i] + '___' + en[i + len(ans):]

SEC = {'dictation': 30, 'choice': 9, 'meaning': 10, 'gap': 20, 'order': 25, 'fix': 30, 'translate': 35, 'shadow': 15, 'cloze': 12}

def item(rule, k, kind):
    name, tag, bank = rule
    en, ru, ans, dis, wrong, hint, alt = bank[k]
    if kind == 'choice':
        opts = shuffle([ans] + dis, en)
        return {'kind': 'choice', 'q': gap_of(en, ans), 'options': opts, 'a': opts.index(ans), 'explain': ru}
    if kind == 'meaning':
        others = [b[1] for j, b in enumerate(bank) if j != k]
        o = shuffle(others, en + 'm')[:2]
        opts = shuffle([ru] + o, en + 'mo')
        return {'kind': 'choice', 'say': en, 'q': L_MEAN, 'options': opts, 'a': opts.index(ru), 'explain': en}
    if kind == 'gap':
        return {'kind': 'gap', 'q': gap_of(en, ans) + ' (' + hint + ')', 'a': [ans] + [x for x in [ans.replace('travelling', 'traveling')] if x != ans], 'explain': ru}
    if kind == 'order':
        return {'kind': 'order', 'en': en, 'ru': ru, 'alt': alt}
    if kind == 'fix':
        assert wrong
        return {'kind': 'fix', 'q': wrong, 'a': [en] + alt, 'explain': ru}
    if kind == 'translate':
        return {'kind': 'translate', 'ru': ru, 'a': [en] + alt}
    if kind == 'shadow':
        return {'kind': 'shadow', 'en': en, 'ru': ru}
    raise ValueError(kind)

L_MEAN = 'Что означает эта фраза?'

def minutes(items):
    return max(2, math.ceil(sum(SEC[i['kind'] if i['kind'] != 'choice' or 'say' not in i else 'meaning'] for i in items) / 60))

def task(tid, ttype, title, items, **kw):
    t = {'id': tid, 'type': ttype, 'title': title, 'minutes': kw.pop('minutes', minutes(items)), 'items': items}
    t.update(kw)
    return t

LESSONS = {
 0: oldt['p1-d1-g1'],
 1: oldt['p1-d2-g1'],
 2: {'type': 'lesson', 'title': 'Фразовые глаголы для работы', 'minutes': 4,
     'body': ['Фразовый глагол = глагол + частица, и смысл часто не складывается из частей: **call off** — не «звать прочь», а «отменить».',
              'Учите их целиком и сразу в предложении, как одно слово. В этом дне 20 глаголов, каждый встретится минимум 4 раза в разных упражнениях.',
              'С местоимением частица встаёт после него: **sort it out**, а не «sort out it». С существительным можно и так, и так: sort out the problem / sort the problem out.',
              'После **look forward to** — форма на **-ing**: looking forward to working with you. Это то же to, что в be used to.'],
     'examples': [{'en': 'They called off the meeting.', 'ru': 'Они отменили встречу.'}, {'en': 'Let\'s put off the launch.', 'ru': 'Давай отложим запуск.'}, {'en': 'She came up with a great idea.', 'ru': 'Она придумала отличную идею.'}, {'en': 'We\'ll sort it out.', 'ru': 'Мы разберёмся.'}, {'en': 'I\'m looking forward to working with you.', 'ru': 'С нетерпением жду совместной работы.'}]},
 3: oldt['p1-d4-g1'],
 4: {'type': 'lesson', 'title': 'Слова-двойники и ложные друзья', 'minutes': 4,
     'body': ['Эти пары похожи по виду, но значат разное. Русскоязычных путают особенно **actual** (= реальный, а не «актуальный») и **sensible** (= разумный, а не «сенситивный»).',
              '**compelling** — убедительный, захватывающий · **compulsory** — обязательный.',
              '**sensible** — разумный, практичный · **sensitive** — чувствительный, деликатный.',
              '**eventually** — в конце концов · **actually** — на самом деле. «Актуальный» = **relevant** или **current**.',
              '**affect** — глагол (влиять) · **effect** — существительное (эффект). **lose** — терять · **loose** — свободный. **borrow** — брать взаймы · **lend** — давать взаймы. **advice** — совет (сущ.) · **advise** — советовать. **economic** — экономический · **economical** — экономичный. **fun** — весёлый, интересный · **funny** — смешной.'],
     'examples': [{'en': 'This topic is still relevant.', 'ru': 'Эта тема всё ещё актуальна.'}, {'en': 'Can I borrow your charger?', 'ru': 'Можно взять твою зарядку?'}, {'en': 'Could you lend me your pen?', 'ru': 'Одолжишь мне ручку?'}, {'en': 'The weather can affect your mood.', 'ru': 'Погода влияет на настроение.'}]},
}

WRITES = [
 ('Своя речь: make и do', 'Напишите 5 предложений о своей неделе, используя сочетания с make и do: make a decision, do research, make progress, do your best, make a mistake…', 'Например: This week I made a decision to…', 30),
 ('Своя речь: раньше и сейчас', 'Напишите о себе: 2 предложения с used to (что было раньше), 2 — с be used to (к чему вы привыкли), 1 — с get used to (к чему привыкаете).', 'I used to… / Now I\'m used to… / I\'m getting used to…', 35),
 ('Своя речь: мой рабочий день', 'Опишите свой рабочий день или прошлую неделю, используя минимум 5 фразовых глаголов из урока.', 'set up, look into, come up with, put off, get back to…', 40),
 ('Своя речь: сожаления и мечты', 'Напишите 4 предложения: одно с wish + Past Simple (о настоящем), два с wish + Past Perfect (о прошлом), одно с If only.', 'I wish I had… / I wish I had done… / If only…', 30),
 ('Своя речь: пары слов', 'Напишите 5 предложений о работе или жизни, правильно используя 5 слов из пар урока (по одному из пяти разных пар).', 'relevant, sensible, affect, borrow, advice…', 35),
 ('Своя речь: сообщение коллеге', 'Напишите коллеге сообщение (около 60 слов) о проекте: что сделано, что отложено, к чему привыкаете в новом процессе, о чём жалеете. Используйте темы недели.', 'made / put off / getting used to / I wish we had…', 55),
 ('Своя речь: итоги недели', 'Напишите по-английски, что за неделю далось легко, что трудно и что хотите повторить (около 50 слов).', 'It was easy to… / I still make mistakes with… / I wish I had…', 45),
]

UX_OLD = {
 0: ['p1-d1-u2'],            # dialog: wireframe review
 1: ['p1-d2-u3'],            # write: Slack
 2: ['p1-d3-u2'],            # dialog: developer vs animations
 3: ['p1-d4-u3'],            # write: client email
 4: [],
 5: ['p1-d5-u2', 'p1-d5-u3'],  # interview dialog + write
}

days = []
used_fmt = {}

def review_items(day_idx, prev_rules, n, seed):
    """interleaved review: earlier rules in formats not used for that sentence yet"""
    cycle = ['translate', 'gap', 'fix', 'order', 'choice', 'meaning']
    out = []
    pool = []
    for r in prev_rules:
        for k in range(40):
            pool.append((r, k))
    pool = shuffle(pool, seed)
    for (r, k) in pool:
        if len(out) >= n:
            break
        done = used_fmt.setdefault((r, k), set())
        for f in shuffle(cycle, f'{seed}{r}{k}'):
            if f in done:
                continue
            if f == 'fix' and not RULES[r][2][k][4]:
                continue
            out.append(item(RULES[r], k, f)); done.add(f); break
    return out

def take(r, ks, fmt):
    res = []
    for k in ks:
        if fmt == 'fix' and not RULES[r][2][k][4]:
            continue
        used_fmt.setdefault((r, k), set()).add(fmt)
        res.append(item(RULES[r], k, fmt))
    return res

for d in range(7):
    day = {'day': d + 1, 'general': [], 'ux': []}
    G = day['general']; U = day['ux']
    gid = lambda n: f'p2-d{d+1}-g{n}'
    uid = lambda n: f'p2-d{d+1}-u{n}'
    if d < 5:
        r = d; name = RULES[r][0]
        day['title'] = ['make или do', 'used to, be used to, get used to', 'Фразовые глаголы для работы', 'wish и if only', 'Слова-двойники'][d]
        les = dict(LESSONS[r]); les['id'] = gid(1); les.pop('items', None)
        G.append(les)
        G.append(task(gid(2), 'mix', 'Узнавание: выберите вариант', take(r, range(0, 10), 'choice')))
        G.append(task(gid(3), 'mix', 'Понимание на слух', take(r, range(10, 16), 'meaning')))
        G.append(task(gid(4), 'gap', 'Впишите нужную форму', take(r, range(16, 26), 'gap')))
        G.append(task(gid(5), 'order', 'Соберите предложение', take(r, range(26, 32), 'order')))
        G.append(task(gid(6), 'fix', 'Найдите и исправьте ошибку', take(r, range(32, 40), 'fix')[:6]))
        G.append(task(gid(7), 'translate', 'Переведите на английский', take(r, list(range(0, 4)) + list(range(16, 20)) + [38, 39], 'translate')))
        G.append(task(gid(8), 'shadow', 'Повторите вслух (shadowing)', take(r, range(26, 34), 'shadow')))
        n = 9
        if d > 0:
            prev = list(range(0, d))
            items = review_items(d, prev, 12 if d < 3 else 14, f'rev{d}')
            G.append(task(gid(n), 'mix', 'Повторение прошлых дней', items)); n += 1
        if d in (0, 2, 4):
            cards = {0: ['g1', 'g2', 'g3', 'g4', 'g5', 'g6'], 2: ['g7', 'g8', 'g9', 'g10', 'g11', 'g12'], 4: ['g13', 'g14', 'g15', 'g16', 'g17', 'g18']}[d]
            G.append({'id': gid(n), 'type': 'cards', 'title': 'Карточки в повторение', 'minutes': 4, 'cards': cards}); n += 1
        w = WRITES[d]
        G.append({'id': gid(n), 'type': 'write', 'title': w[0], 'minutes': 6, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})
    elif d == 5:
        day['title'] = 'Большое повторение'
        G.append(task(gid(1), 'mix', 'Смешанная практика: все правила', review_items(d, [0, 1, 2, 3, 4], 30, 'big6')))
        dict_items = []
        for (r, k) in [(0, 6), (1, 2), (2, 12), (3, 0), (4, 12), (1, 30), (2, 18), (3, 3)]:
            en = RULES[r][2][k][0]
            dict_items.append({'kind': 'dictation', 'say': en, 'a': [en] + RULES[r][2][k][6]})
        G.append(task(gid(2), 'dictation', 'Диктант по всем темам', dict_items, minutes=5))
        G.append(task(gid(3), 'translate', 'Перевод: все темы вперемешку', review_items(d, [0, 1, 2, 3, 4], 12, 'tr6')))
        G.append(task(gid(4), 'shadow', 'Повторите вслух', [item(RULES[r], k, 'shadow') for (r, k) in [(0, 0), (1, 1), (2, 18), (3, 2), (4, 12), (1, 6), (2, 12), (3, 12)]]))
        w = WRITES[5]
        G.append({'id': gid(5), 'type': 'write', 'title': w[0], 'minutes': 8, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})
    else:
        day['title'] = 'Итог недели'
        G.append(task(gid(1), 'mix', 'Различаем похожее: used to / wish / пары', review_items(d, [1, 3, 4], 18, 'fin7')))
        G.append(task(gid(2), 'mix', 'Итоговая практика: make/do и фразовые', review_items(d, [0, 2], 14, 'fin7b')))
        G.append(task(gid(3), 'translate', 'Итоговый перевод', review_items(d, [0, 1, 2, 3, 4], 14, 'tr7')))
        w = WRITES[6]
        G.append({'id': gid(4), 'type': 'write', 'title': w[0], 'minutes': 7, 'prompt': w[1], 'hint': w[2], 'minWords': w[3]})

    # ---------- UX ----------
    if d < 6:
        th, ph = UX[d]
        U.append({'id': uid(1), 'type': 'lesson', 'title': 'Фразы: ' + th.lower(), 'minutes': 4,
                  'body': ['Сегодня 16 рабочих фраз. Сначала прослушайте каждую и повторите вслух, потом они встретятся в упражнениях ещё 3–4 раза.'],
                  'examples': [{'en': e, 'ru': r} for e, r in ph]})
        mean = []
        for k in range(0, 8):
            e, r = ph[k]
            others = shuffle([x[1] for j, x in enumerate(ph) if j != k], e)[:2]
            opts = shuffle([r] + others, e + 'u')
            mean.append({'kind': 'choice', 'say': e, 'q': L_MEAN, 'options': opts, 'a': opts.index(r), 'explain': e})
        U.append(task(uid(2), 'mix', 'Понимание на слух', mean))
        U.append(task(uid(3), 'translate', 'Переведите на английский', [{'kind': 'translate', 'ru': r, 'a': [e]} for e, r in ph[0:8]]))
        U.append(task(uid(4), 'order', 'Соберите фразу', [{'kind': 'order', 'en': e, 'ru': r} for e, r in ph[8:14]]))
        U.append(task(uid(6), 'shadow', 'Повторите вслух', [{'kind': 'shadow', 'en': e, 'ru': r} for e, r in ph[0:16:2]]))
        n = 7
        if d in (0, 3):
            U.append({'id': uid(n), 'type': 'cards', 'title': 'Слова для работы', 'minutes': 4, 'cards': ['u1', 'u2', 'u3', 'u4', 'u5', 'u6'] if d == 0 else ['u7', 'u8', 'u9', 'u10', 'u11', 'u12']}); n += 1
        for oid in UX_OLD[d]:
            t = dict(oldt[oid]); t['id'] = uid(n); n += 1; U.append(t)
        if d == 4:
            U.append({'id': uid(n), 'type': 'write', 'title': 'Сообщение после созвона', 'minutes': 6, 'prompt': 'Напишите в Slack итог созвона с командой: что решили, кто что делает, когда следующая встреча (40–60 слов).', 'hint': 'To sum up… / I\'ll share… / Let\'s schedule…', 'minWords': 40})
        if d > 0:
            prev = [x for i in range(d) for x in UX[i][1]]
            pk = shuffle(prev, f'uxrev{d}')[:8]
            U.append(task(uid(n + 1), 'translate', 'Повторение фраз прошлых дней', [{'kind': 'translate', 'ru': r, 'a': [e]} for e, r in pk]))
    else:
        allp = [x for i in range(6) for x in UX[i][1]]
        pk = shuffle(allp, 'ux7')
        U.append(task(uid(1), 'translate', 'Итог: рабочие фразы', [{'kind': 'translate', 'ru': r, 'a': [e]} for e, r in pk[:14]]))
        U.append(task(uid(2), 'order', 'Итог: соберите фразы', [{'kind': 'order', 'en': e, 'ru': r} for e, r in pk[14:22]]))
        U.append(task(uid(3), 'shadow', 'Итог: повторите вслух', [{'kind': 'shadow', 'en': e, 'ru': r} for e, r in pk[22:32]]))
    days.append(day)

# ---------- media ----------
AV = [
 ('a1', 'silo', 'изолированная команда, «силос»', 'Designers worked in silos and rarely saw each other\'s work.', 'C1'),
 ('a2', 'ad hoc', 'спонтанный, по случаю', 'We only had ad hoc feedback sessions.', 'C1'),
 ('a3', 'constructive feedback', 'конструктивный фидбэк', 'Constructive feedback helps you improve the design.', 'B2'),
 ('a4', 'low turnout', 'мало участников, низкая явка', 'The session was cancelled because of low turnout.', 'C1'),
 ('a5', 'pinpoint', 'точно определить', 'The crit helped her pinpoint where she needed help.', 'C1'),
 ('a6', 'prioritise', 'расставлять приоритеты', 'We prioritise the actions with the whole team.', 'B2'),
 ('a7', 'backlog', 'бэклог, список задач', 'All actions go into the delivery backlog.', 'pro'),
 ('a8', 'two-way conversation', 'диалог, разговор в обе стороны', 'Feedback should be a two-way conversation.', 'B2'),
 ('a9', 'ingrained', 'укоренившийся', 'Old habits are deeply ingrained.', 'C2'),
 ('a10', 'effortlessly', 'без усилий', 'After a while, the habit happens effortlessly.', 'C1'),
 ('a11', 'plateau', 'выйти на плато, перестать расти', 'Progress plateaued after about two months.', 'C1'),
 ('a12', 'consistently', 'последовательно, постоянно', 'You need to practise consistently.', 'B2'),
 ('a13', 'cue', 'сигнал, триггер', 'Link the new habit to a daily cue.', 'C1'),
 ('a14', 'rigorous', 'строгий, тщательный', 'The idea was not based on rigorous research.', 'C1'),
 ('a15', 'interplay', 'взаимодействие', 'There is a complex interplay of factors.', 'C2'),
 ('a16', 'one-size-fits-all', 'универсальный, одинаковый для всех', 'There is no one-size-fits-all approach.', 'C1'),
]
media = [
 {'id': 'art-design-crits', 'kind': 'article', 'topic': 'ux', 'title': 'How a team built a culture of design crits',
  'source': 'ESFA Digital blog (GOV.UK)', 'author': 'Jaskiran Kang', 'published': '15.01.2020', 'level': 'B2', 'minutes': 25,
  'url': 'https://sfadigital.blog.gov.uk/2020/01/15/how-the-apprenticeship-service-has-been-creating-a-culture-of-design-crits',
  'about': 'Ведущий дизайнер государственного сервиса рассказывает, как команда перешла от случайного фидбэка к регулярным дизайн-критикам: какой формат придумали, что пошло не так и что получилось. Много живой лексики для ревью.',
  'note': 'Вопросы составлены по статье своими словами, текст статьи здесь не копируется.',
  'tasks': [
   {'id': 'm1-1', 'type': 'cards', 'title': 'Слова до чтения', 'minutes': 4, 'cards': ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']},
   {'id': 'm1-2', 'type': 'quiz', 'title': 'Понимание статьи', 'minutes': 8, 'items': [
     {'q': 'Before the change, how did designers usually get feedback?', 'options': ['In weekly formal reviews', 'Ad hoc, from friendly colleagues or on Slack', 'Only from users'], 'a': 1, 'explain': 'Фидбэк был случайным: от знакомых коллег лично или в Slack.'},
     {'q': 'What was a problem with that feedback?', 'options': ['It came too late and reached only a few people', 'It was too formal', 'It was always negative'], 'a': 0, 'explain': 'Он доходил до немногих и редко приходил на раннем этапе.'},
     {'q': 'Which goal did the team set?', 'options': ['To hire more designers', 'To get designers to share work early', 'To stop using sticky notes'], 'a': 1, 'explain': 'Одна из трёх целей — делиться работой рано.'},
     {'q': 'How long was the crit session they adapted?', 'options': ['15 minutes', '45 minutes', 'Two hours'], 'a': 1, 'explain': 'Формат на 45 минут: показ, разбор фидбэка, темы и действия.'},
     {'q': 'What is the "golden rule" of their crits?', 'options': ['Always agree with the lead', 'You are not your design', 'Never show unfinished work'], 'a': 1, 'explain': 'Критикуют работу, а не человека.'},
     {'q': 'What went wrong at the start?', 'options': ['Sessions were cancelled because few people came', 'Managers banned the sessions', 'The room was too small'], 'a': 0, 'explain': 'Несколько сессий отменили из-за низкой явки.'},
     {'q': 'How did the author fix that problem?', 'options': ['By making crits compulsory', 'Through one-to-one conversations about a safe, supportive space', 'By offering free lunch'], 'a': 1, 'explain': 'Личные разговоры с дизайнерами о том, что это безопасное пространство.'},
     {'q': 'What happens with the actions after a crit?', 'options': ['They are forgotten', 'They go into the delivery backlog and are prioritised with the team', 'Only the presenter sees them'], 'a': 1, 'explain': 'Действия попадают в бэклог и приоритизируются.'}]},
   task('m1-3', 'translate', 'Перевод с новыми словами', [
     {'kind': 'translate', 'ru': 'Наши дизайнеры работали изолированно.', 'a': ['Our designers worked in silos.', 'Our designers were working in silos.']},
     {'kind': 'translate', 'ru': 'Мне нужен конструктивный фидбэк.', 'a': ['I need constructive feedback.']},
     {'kind': 'translate', 'ru': 'Встречу отменили из-за низкой явки.', 'a': ['The meeting was cancelled because of low turnout.', 'The meeting was called off because of low turnout.', 'The meeting was cancelled due to low turnout.']},
     {'kind': 'translate', 'ru': 'Это помогло мне точно понять, где мне нужна помощь.', 'a': ['It helped me pinpoint where I needed help.', 'This helped me pinpoint where I needed help.']},
     {'kind': 'translate', 'ru': 'Давайте расставим приоритеты вместе с командой.', 'a': ['Let\'s prioritise with the team.', 'Let\'s prioritise together with the team.']},
     {'kind': 'translate', 'ru': 'Фидбэк должен быть диалогом.', 'a': ['Feedback should be a two-way conversation.']}]),
   {'id': 'm1-4', 'type': 'write', 'title': 'Пересказ и мнение', 'minutes': 8, 'prompt': 'Перескажите статью своими словами (3–4 предложения) — можно вслух через «Надиктовать» и ответьте: сработал бы такой формат в вашей команде? Почему?', 'hint': 'The article is about… / The team… / In my team, this would…', 'minWords': 70},
  ]},
 {'id': 'art-habits', 'kind': 'article', 'topic': 'general', 'title': 'Forming useful habits is harder than we think',
  'source': 'The Irish Times', 'author': 'William Reville', 'published': '01.05.2025', 'level': 'B2–C1', 'minutes': 25,
  'url': 'https://www.irishtimes.com/science/2025/05/01/forming-useful-habits-not-as-easy-as-widely-believed',
  'about': 'Почему правило «21 дня» — миф и сколько на самом деле занимает формирование привычки по данным исследований. Тема прямо про вас: автоматизм в английском строится так же.',
  'note': 'Вопросы составлены по статье своими словами, текст статьи здесь не копируется.',
  'tasks': [
   {'id': 'm2-1', 'type': 'cards', 'title': 'Слова до чтения', 'minutes': 4, 'cards': ['a9', 'a10', 'a11', 'a12', 'a13', 'a14', 'a15', 'a16']},
   {'id': 'm2-2', 'type': 'quiz', 'title': 'Понимание статьи', 'minutes': 8, 'items': [
     {'q': 'According to the article, what makes a habit form?', 'options': ['Strong willpower alone', 'Repeating a behaviour in a stable context', 'Doing something once, very intensely'], 'a': 1, 'explain': 'Повторение в одном и том же контексте связывает сигнал и действие.'},
     {'q': 'Where does the "21 days" idea come from?', 'options': ['A large controlled trial', 'A surgeon\'s observations of his patients in 1960', 'A university survey'], 'a': 1, 'explain': 'Из наблюдений хирурга Максвелла Мольца, а не из строгих исследований.'},
     {'q': 'How many students took part in the main study?', 'options': ['About 20', 'About 100', 'About 1,000'], 'a': 1, 'explain': '96 студентов.'},
     {'q': 'On average, when did automaticity stop growing?', 'options': ['After about 21 days', 'After about 66 days', 'After about a year'], 'a': 1, 'explain': 'В среднем около 66 дней.'},
     {'q': 'Which habits took longer to form?', 'options': ['Drinking habits', 'Eating habits', 'Exercise habits'], 'a': 2, 'explain': 'Привычки, связанные со спортом, формировались дольше.'},
     {'q': 'What happened to almost half of the participants?', 'options': ['They formed a habit in a week', 'They were not consistent enough to form a habit', 'They left the study on day one'], 'a': 1, 'explain': 'Почти половина действовала недостаточно последовательно.'},
     {'q': 'What did a later review of studies find?', 'options': ['Habits take about two to five months', 'Habits always take exactly 66 days', 'Habits cannot be changed'], 'a': 0, 'explain': 'От двух до пяти месяцев, и у всех по-разному.'},
     {'q': 'Which practical tip is in the article?', 'options': ['Link the new behaviour to a daily cue', 'Change your routine every day', 'Rely only on motivation'], 'a': 0, 'explain': 'Привязать новое действие к ежедневному сигналу.'}]},
   task('m2-3', 'translate', 'Перевод с новыми словами', [
     {'kind': 'translate', 'ru': 'Эта привычка глубоко укоренилась.', 'a': ['This habit is deeply ingrained.', 'The habit is deeply ingrained.']},
     {'kind': 'translate', 'ru': 'Через некоторое время это происходит без усилий.', 'a': ['After a while, it happens effortlessly.', 'After some time, it happens effortlessly.']},
     {'kind': 'translate', 'ru': 'Нужно заниматься последовательно.', 'a': ['You need to practise consistently.', 'You need to practice consistently.', 'You have to practise consistently.']},
     {'kind': 'translate', 'ru': 'Привяжи новую привычку к ежедневному сигналу.', 'a': ['Link the new habit to a daily cue.', 'Tie the new habit to a daily cue.']},
     {'kind': 'translate', 'ru': 'Универсального подхода не существует.', 'a': ['There is no one-size-fits-all approach.', 'There\'s no one-size-fits-all approach.']},
     {'kind': 'translate', 'ru': 'Мой прогресс вышел на плато.', 'a': ['My progress has plateaued.', 'My progress plateaued.']}]),
   {'id': 'm2-4', 'type': 'write', 'title': 'Моя привычка', 'minutes': 8, 'prompt': 'Какую привычку вы сейчас формируете (например, английский каждый день)? Опишите сигнал, действие и что мешает. Используйте минимум 4 слова из статьи.', 'hint': 'My cue is… / I try to practise consistently… / There is no one-size-fits-all…', 'minWords': 60},
  ]},
 {'id': 'pod-6min', 'kind': 'podcast', 'topic': 'general', 'title': '6 Minute English', 'source': 'BBC Learning English', 'level': 'B1–B2', 'minutes': 20,
  'url': 'https://podcasts.apple.com/podcast/262026947?l=en',
  'about': 'Короткие выпуски: два ведущих 6 минут обсуждают одну тему и разбирают несколько полезных слов. Удобно слушать в дороге. Выбирайте любой свежий выпуск.',
  'note': 'Расшифровки выпусков мне отсюда недоступны, поэтому задания общие. Запишите слова из выпуска в задании 2 и пришлите экспорт — по ним я соберу упражнения.',
  'tasks': [
   {'id': 'm3-1', 'type': 'lesson', 'title': 'Как слушать подкаст', 'minutes': 2, 'body': [
     '**1-й раз** — просто слушайте, не останавливаясь. Цель — понять тему и общий смысл.',
     '**2-й раз** — останавливайте и записывайте слова, которые разбирают ведущие, и фразы, которые не поняли.',
     '**3-й раз** — включите 30 секунд любимого куска и повторяйте за ведущими вслух (shadowing).'], 'examples': []},
   {'id': 'm3-2', 'type': 'write', 'title': 'Слова выпуска', 'minutes': 8, 'prompt': 'Напишите название выпуска и слова, которые разбирали ведущие (обычно их около шести), — к каждому слову пример из выпуска или свой.', 'hint': 'Episode: … / 1. … — …', 'minWords': 25},
   {'id': 'm3-3', 'type': 'write', 'title': 'Пересказ выпуска вслух', 'minutes': 6, 'prompt': 'Перескажите вслух, о чём был выпуск, в 3–5 предложениях — нажмите «Надиктовать» и говорите по-английски. Используйте минимум 2 слова из выпуска. Потом поправьте текст, если распознавание ошиблось.', 'hint': 'The episode is about… / They discuss… / I learned that…', 'minWords': 40},
  ]},
]

old_vocab = OLD['vocab']
vocab = old_vocab + [{'id': i, 'en': e, 'ru': r, 'ex': x, 'lvl': l, 'tag': 'media'} for i, e, r, x, l in AV]

pack = {'type': 'study-pack', 'version': 1, 'id': 'pack-002', 'replaces': ['pack-001'],
        'title': 'Неделя 1 · плотная: make/do, used to, фразовые, wish, двойники', 'level': 'B1', 'created': '2026-10-30',
        'method': 'Этапы освоения навыка (правило → контролируемая практика → своя речь), интервальное повторение правил на следующих днях, смешанные упражнения для похожих правил, shadowing.',
        'vocab': vocab, 'days': days, 'media': media}

# stats + checks
tot = 0
for dd in days:
    m = sum(t['minutes'] for t in dd['general'] + dd['ux'])
    n = sum(len(t.get('items', [])) for t in dd['general'] + dd['ux'])
    ids = [t['id'] for t in dd['general'] + dd['ux']]
    assert len(ids) == len(set(ids))
    print(dd['day'], dd['title'], f'{m} мин', f'{n} заданий', 'общий', sum(t['minutes'] for t in dd['general']), 'ux', sum(t['minutes'] for t in dd['ux']))
    tot += n
print('total items', tot)
allids = [t['id'] for dd in days for t in dd['general'] + dd['ux']] + [t['id'] for m in media for t in m['tasks']]
assert len(allids) == len(set(allids))
V = {v['id'] for v in vocab}
for dd in days:
    for t in dd['general'] + dd['ux']:
        for c in t.get('cards', []): assert c in V, c
        for it in t.get('items', []):
            if 'options' in it: assert 0 <= it['a'] < len(it['options'])
json.dump(pack, open('/home/claude/pack-002.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(json.dumps(pack, ensure_ascii=False)) // 1024, 'KB')
