"""pack-003n → pack-003o (23.11.2026): дни 4–7 по новой схеме (её решение 23.11).
Д4–д5: ядро ≈ 25 мин (урок, узнавание, диалог, перевод + UX урок и на слух), остальное — optional.
Д6: «Слабое — в новых форматах» (редактор, ответь в чате, скажи иначе, сценки-квесты); старые задания — optional.
Д7: свежая тема «Почему мы откладываем дела»; старые итоговые задания — optional.
Задания с прежними id сохраняют прогресс. Запуск: python3 tools/content/rework_d4_7.py
"""
import json, os
R = os.path.join(os.path.dirname(__file__), '..', '..', 'packs')
p = json.load(open(os.path.join(R, 'pack-003n.json')))
p['id'] = 'pack-003o'
p['replaces'] = p['replaces'] + ['pack-003n']
p['created'] = '2026-11-23'

CORE = {
    4: {'p3-d4-g1', 'p3-d4-g2', 'p3-d4-g20', 'p3-d4-g7', 'p3-d4-u1', 'p3-d4-u2'},
    5: {'p3-d5-g1', 'p3-d5-g2', 'p3-d5-g20', 'p3-d5-g7', 'p3-d5-u1', 'p3-d5-u2'},
    6: set(), 7: set(),
}

def ch(q, opts, a, explain, why, rule):
    return {'kind': 'choice', 'q': q, 'options': opts, 'a': a, 'explain': explain, 'why': why, 'rule': rule}

W = 'p3-d6-g30'  # урок дня 6 — правило для тегов
D6_NEW = [
    {'id': W, 'type': 'lesson', 'title': 'Четыре вещи, которые ломаются чаще всего', 'minutes': 4, 'body': [
        'Сегодня не новое правило, а ваши частые ошибки — в новых форматах: редактор, ответ в чате, «скажи иначе», сценки. Сначала четыре короткие логики.',
        '**1. Вопрос.** Есть глагол действия → do / does / did + начальная форма: **Did** it **take** long? What **do** you **mean**? Глагола действия нет → be: What time **is** the call? Where **is** the file?',
        '**2. is или глагол.** Глагол действия стоит сам, is ему не нужен: The menu **opens** on hover. It **works**. is — только когда глагола нет: It**\'s** fast. It**\'s** open.',
        '**3. Артикли.** a — «один из, какой-то»: **a** quick question, **a** tight deadline. the — понятно, какой именно: **the** top bar, **the** design, sorry for **the** late reply. Без артикля, если уже есть чей: **our** app, **your** first task (не the your).',
        '**4. Фразовый глагол — обычный глагол.** Он меняет время, как все: turn down → **turned** down, bring up → **brought** up, put off → put off (неправильный). После did / can / have to — начальная форма: did you **find** out, we can **call** it off. После stop / give up / carry on — **-ing**: Stop **putting** it off.',
    ], 'examples': [
        {'en': 'Did it take long?', 'ru': 'Это заняло много времени?'},
        {'en': 'What time is the call?', 'ru': 'Во сколько созвон?'},
        {'en': 'The menu opens on hover.', 'ru': 'Меню открывается при наведении.'},
        {'en': 'Sorry for the late reply.', 'ru': 'Извините за поздний ответ.'},
        {'en': 'The client turned down our offer.', 'ru': 'Клиент отклонил наше предложение.'},
        {'en': 'Stop putting it off!', 'ru': 'Хватит это откладывать!'},
    ]},
    {'id': 'p3-d6-g31', 'type': 'fix', 'title': 'Будь редактором: сообщения коллег', 'minutes': 4, 'items': [
        {'kind': 'fix', 'q': 'Hi! What time does the call today?', 'a': ['Hi! What time is the call today?'], 'explain': 'Привет! Во сколько сегодня созвон?', 'rule': W, 'why': 'Глагола действия нет → be: What time is…'},
        {'kind': 'fix', 'q': "The new menu it's opens on hover.", 'a': ['The new menu opens on hover.'], 'explain': 'Новое меню открывается при наведении.', 'rule': W, 'why': 'opens — глагол действия: ни it, ни is не нужны'},
        {'kind': 'fix', 'q': 'Sorry for late reply, I was on a call.', 'a': ['Sorry for the late reply, I was on a call.', 'Sorry for the late reply. I was on a call.'], 'explain': 'Извините за поздний ответ, я была на созвоне.', 'rule': W, 'why': 'Понятно, какой ответ — мой → the late reply'},
        {'kind': 'fix', 'q': 'The client turn down our offer yesterday.', 'a': ['The client turned down our offer yesterday.', 'The client turned our offer down yesterday.'], 'explain': 'Клиент вчера отклонил наше предложение.', 'rule': W, 'why': 'yesterday → прошедшее: turned down'},
        {'kind': 'fix', 'q': "Did you found out why the button doesn't work?", 'a': ["Did you find out why the button doesn't work?", "Did you find out why the button does not work?"], 'explain': 'Ты выяснила, почему кнопка не работает?', 'rule': W, 'why': 'После did — начальная форма: find'},
        {'kind': 'fix', 'q': 'Please stop to put off the hard tasks.', 'a': ['Please stop putting off the hard tasks.', 'Please stop putting the hard tasks off.'], 'explain': 'Пожалуйста, перестань откладывать трудные задачи.', 'rule': W, 'why': 'stop + -ing = перестать делать'},
    ]},
    {'id': 'p3-d6-g32', 'type': 'translate', 'title': 'Ответь в чате (неформально)', 'minutes': 6, 'items': [
        {'kind': 'translate', 'ru': 'Коллега: «hey, quick q — did u get my file?» Ответьте: Да, получила! Посмотрю после обеда.', 'a': ["Yes, got it! I'll take a look after lunch.", "Yes, I got it. I'll look at it after lunch.", "Got it, thanks! I'll check it after lunch."], 'rule': W, 'why': 'В чате коротко: Got it! I\'ll take a look…'},
        {'kind': 'translate', 'ru': 'Коллега: «can u join the call at 3?» Ответьте: Конечно, буду через 5 минут.', 'a': ["Sure, I'll be there in 5 minutes.", "Sure, I'll join in five minutes.", 'Sure, see you in 5 min!'], 'rule': W, 'why': 'через 5 минут = in 5 minutes (не after)'},
        {'kind': 'translate', 'ru': 'Коллега: «we got the new client!! 🎉» Ответьте: Поздравляю, отличная новость!', 'a': ["Congrats! That's great news!", "Congratulations, that's great news!", 'Wow, congrats! Great news!'], 'rule': W, 'why': 'Неформально: Congrats! (не my celebrations)'},
        {'kind': 'translate', 'ru': 'Коллега: «sorry, can we move our call to tomorrow?» Ответьте: Без проблем! Какое время тебе удобно?', 'a': ['No worries! What time works for you?', 'No problem! What time works for you?', 'Sure! What time is good for you?'], 'rule': W, 'why': 'What time works for you? — есть глагол works, без do'},
        {'kind': 'translate', 'ru': 'Коллега: «did the test take long?» Ответьте: Нет, минут 20. Все пять участников справились.', 'a': ['No, about 20 minutes. All five participants did fine.', 'Not really, about twenty minutes. All five participants managed.', 'No, around 20 minutes. All five participants got through it.'], 'rule': W, 'why': 'участники теста — participants'},
        {'kind': 'translate', 'ru': 'Коллега: «what do u mean by "too busy"?» Ответьте: Я имею в виду, что на экране слишком много кнопок.', 'a': ['I mean there are too many buttons on the screen.', 'I mean the screen has too many buttons.', 'I mean that there are too many buttons on the screen.'], 'rule': W, 'why': 'there are + много чего-то; I mean — без is'},
    ]},
    {'id': 'p3-d6-g33', 'type': 'gap', 'title': 'Скажи иначе: фразовые глаголы', 'minutes': 4, 'items': [
        {'kind': 'gap', 'q': 'We postponed the meeting. = We ___ the meeting. (put / off — прошедшее)', 'a': ['put off'], 'explain': 'Мы отложили встречу.', 'rule': W, 'why': 'put — неправильный: put – put – put; off = «отодвинуть»'},
        {'kind': 'gap', 'q': 'The bank said no to our request. = The bank ___ our request. (turn / down — прошедшее)', 'a': ['turned down'], 'explain': 'Банк отклонил нашу заявку.', 'rule': W, 'why': 'Прошлое → turned down'},
        {'kind': 'gap', 'q': 'We cancelled the workshop. = We ___ the workshop. (call / off — прошедшее)', 'a': ['called off'], 'explain': 'Мы отменили воркшоп.', 'rule': W, 'why': 'Отменить = call off; отложить = put off'},
        {'kind': 'gap', 'q': 'I need to understand why it crashes. = I need to ___ why it crashes. (find / out)', 'a': ['find out', 'figure out'], 'explain': 'Мне нужно выяснить, почему оно падает.', 'rule': W, 'why': 'После need to — начальная форма'},
        {'kind': 'gap', 'q': 'It was necessary for us to rewrite the text. = We ___ rewrite the text. (have to — прошедшее)', 'a': ['had to'], 'explain': 'Нам пришлось переписать текст.', 'rule': W, 'why': '«Пришлось» = had to (не were needed to)'},
        {'kind': 'gap', 'q': "Don't postpone it any more! = Stop ___ it off! (put)", 'a': ['putting'], 'explain': 'Хватит это откладывать!', 'rule': W, 'why': 'stop + -ing'},
    ]},
    {'id': 'p3-d6-g34', 'type': 'mix', 'title': 'Сценка: созвон с клиентом', 'minutes': 4, 'items': [
        ch("The call starts. You can't hear the client well. What do you say?", ["You speak bad, repeat.", "Sorry, I can't hear you very well — could you say that again?", "I don't listen you."], 1, 'Извините, я плохо вас слышу — можете повторить?', 'hear — слышать (не listen); вежливо: could you…', W),
        ch('You want to show your design.', ['Let me share my screen.', 'I share you my screen.', 'Look at my screen now.'], 0, 'Давайте я покажу свой экран.', 'Let me + глагол — вежливо предложить', W),
        ch('The client asks for a big change one day before the deadline.', ['No. It is too late.', 'You are not right.', 'I see your point, but it might be worth discussing the timeline first.'], 2, 'Понимаю вас, но, возможно, стоит сначала обсудить сроки.', 'I see your point, but… — несогласие мягко; worth + -ing', W),
        ch("You didn't understand what the client meant.", ['What you mean?', 'Just to clarify — do you mean the main page or the whole app?', 'Explain normally, please.'], 1, 'Просто уточню — вы имеете в виду главную страницу или всё приложение?', 'Just to clarify… + вопрос с do', W),
        ch('The client found a small mistake in your design.', ["It's not my mistake.", 'Good catch, I fix it yesterday.', "Good catch, thanks! I'll fix it today."], 2, 'Хорошо подмечено, спасибо! Исправлю сегодня.', "Good catch — «хорошо заметили»; будущее — I'll fix", W),
        ch('You need time to think before you answer.', ['Let me think about it and get back to you tomorrow.', 'I will answer you after.', 'Let me think and I come back to you.'], 0, 'Дайте подумать, я вернусь к вам завтра.', 'get back to you — вернуться с ответом', W),
    ]},
]
D6_UX = [
    {'id': 'p3-d6-u10', 'type': 'mix', 'title': 'Сценка: вы проводите юзабилити-тест', 'minutes': 4, 'items': [
        ch('The participant joins the call. You start.', ['Thank you that you came.', 'Thanks for taking the time to join us today.', 'Good that you are here today.'], 1, 'Спасибо, что нашли время присоединиться сегодня.', 'Thanks for + -ing', W),
        ch('The participant looks nervous.', ["There are no right or wrong answers — we're testing the design, not you.", 'There are no true or false answers, we test not you.', "You can't make mistakes because we test design."], 0, 'Здесь нет правильных и неправильных ответов — мы тестируем дизайн, а не вас.', 'right or wrong; the design, not you', W),
        ch('You want the participant to say what they are thinking.', ['Please tell aloud what you think.', 'Please speak your thoughts loud.', 'Please think aloud while you go through the app.'], 2, 'Пожалуйста, размышляйте вслух, пока проходите приложение.', 'think aloud — устойчивое выражение', W),
        ch("The participant can't find the button and stops.", ['Faster please, where do you click?', 'Take your time. Where would you tap next?', "Why you don't see the button?"], 1, 'Не торопитесь. Куда бы вы нажали дальше?', 'Where would you tap next? — нейтральный вопрос без подсказки', W),
        ch('You report the result to the team.', ["Three of five recipients didn't find filter.", 'Three from five users not found the filter.', "Three out of five participants couldn't find the filter."], 2, 'Трое из пяти участников не смогли найти фильтр.', 'three out of five; participants; couldn\'t find', W),
        ch('The test is over.', ["That's all from me — thank you, this was really helpful.", "It's all. You are free.", 'Finish. Thank you for helping.'], 0, 'Это всё с моей стороны — спасибо, это было очень полезно.', "That's all (не It's all)", W),
    ]},
]

L7 = 'p3-d7-g40'
D7_NEW = [
    {'id': L7, 'type': 'lesson', 'title': 'Свежая тема: почему мы откладываем дела', 'minutes': 5, 'body': [
        'Новая тема вместо очередного правила. Прочитайте короткий текст (его можно прослушать по примерам ниже), потом — вопросы, диалог и переписка. Старые правила здесь тоже есть: put off, -ing, Present Perfect, вопросы.',
        'Most of us put things off from time to time. We know the task is important, but we check our email, make coffee or clean the desk instead.',
        "Researchers say that procrastination isn't really about laziness. It's about feelings. When a task feels boring, difficult or unclear, we feel bad, so we avoid it to feel better right now. The problem is that the good feeling doesn't last, and later we feel guilty.",
        "So what helps? First, break a big task into small steps: 'write the report' is scary, but 'write three bullet points' is easy. Second, start with just five minutes — starting is usually the hardest part. Third, be kind to yourself. People who forgive themselves for procrastinating are less likely to do it again.",
        'Слова: **put off** — откладывать; **avoid** — избегать; **laziness** — лень; **guilty** — виноватый; **last** (глагол) — длиться; **break into steps** — разбить на шаги; **forgive** — прощать; **be less likely to** — с меньшей вероятностью.',
    ], 'examples': [
        {'en': 'Most of us put things off from time to time.', 'ru': 'Большинство из нас время от времени откладывает дела.'},
        {'en': "Procrastination isn't really about laziness. It's about feelings.", 'ru': 'Прокрастинация — на самом деле не про лень. Она про чувства.'},
        {'en': "The good feeling doesn't last, and later we feel guilty.", 'ru': 'Хорошее чувство не длится долго, а потом нам стыдно.'},
        {'en': 'Break a big task into small steps.', 'ru': 'Разбейте большую задачу на маленькие шаги.'},
        {'en': 'Starting is usually the hardest part.', 'ru': 'Начать — обычно самое трудное.'},
    ]},
    {'id': 'p3-d7-g41', 'type': 'mix', 'title': 'Вопросы по тексту', 'minutes': 3, 'items': [
        ch('According to the text, procrastination is mainly about…', ['laziness', 'feelings', 'bad planning'], 1, 'Прокрастинация — в основном про чувства.', "It's about feelings.", L7),
        ch('Why do we avoid a difficult task?', ['To feel better right now', 'To save time', 'Because the deadline is far away'], 0, 'Чтобы почувствовать себя лучше прямо сейчас.', 'we avoid it to feel better right now', L7),
        ch('What happens to the good feeling?', ['It lasts all day.', "It doesn't last.", 'It helps us finish.'], 1, 'Хорошее чувство быстро проходит.', "the good feeling doesn't last", L7),
        ch('What is the first tip?', ['Start with the hardest step.', 'Work without breaks.', 'Break a big task into small steps.'], 2, 'Разбить большую задачу на маленькие шаги.', 'First, break a big task into small steps', L7),
        ch('Why start with just five minutes?', ['Starting is usually the hardest part.', 'Five minutes is enough for most tasks.', 'Short tasks are more fun.'], 0, 'Начать — обычно самое трудное.', 'starting is usually the hardest part', L7),
        ch('People who forgive themselves for procrastinating…', ['procrastinate more.', 'feel more guilty.', 'are less likely to do it again.'], 2, 'С меньшей вероятностью сделают это снова.', 'are less likely to do it again', L7),
    ]},
    {'id': 'p3-d7-g42', 'type': 'dialog', 'title': 'Диалог: презентация на завтра', 'minutes': 5, 'lines': [
        {'s': 'Mia', 't': 'You look tired. Is everything OK?'},
        {'s': 'Tom', 't': "Not really. I've put off the presentation for a week, and now it's due tomorrow."},
        {'s': 'Mia', 't': "Oh no. What's the hardest part?"},
        {'s': 'Tom', 't': 'Starting, I think. The whole thing feels huge.'},
        {'s': 'Mia', 't': "Why don't you break it into steps? Just do the first three slides tonight."},
        {'s': 'Tom', 't': "Good idea. And I'll turn off my phone for an hour."},
    ], 'items': [
        {'q': "When is Tom's presentation due?", 'options': ['Tonight', 'Tomorrow', 'In a week'], 'a': 1, 'explain': "it's due tomorrow — срок завтра", 'why': 'due + время = срок сдачи', 'rule': L7},
        {'q': 'How long has Tom put off the presentation?', 'options': ['For a day', 'Since the morning', 'For a week'], 'a': 2, 'explain': "I've put off the presentation for a week.", 'why': 'Present Perfect + for = до сих пор, в течение', 'rule': L7},
        {'q': 'What is the hardest part for Tom?', 'options': ['Starting', 'Finishing', 'Designing the slides'], 'a': 0, 'explain': 'Starting, I think.', 'why': 'starting — -ing как подлежащее', 'rule': L7},
        {'q': 'What will Tom do tonight?', 'options': ['Finish all the slides', 'Do the first three slides', 'Call Mia'], 'a': 1, 'explain': 'Just do the first three slides tonight.', 'why': 'Совет Мии: начать с маленького шага', 'rule': L7},
    ]},
    {'id': 'p3-d7-g43', 'type': 'translate', 'title': 'Ответь в чате: про откладывание', 'minutes': 4, 'items': [
        {'kind': 'translate', 'ru': 'Друг: «how\'s the report going?» Ответьте: Честно? Я откладываю его уже три дня.', 'a': ["Honestly? I've been putting it off for three days.", "To be honest, I've put it off for three days.", "Honestly, I've been putting it off for 3 days."], 'rule': L7, 'why': 'уже три дня → have been + -ing / have put off + for'},
        {'kind': 'translate', 'ru': 'Друг: «same here 😅 any tips?» Ответьте: Разбей его на маленькие шаги и начни с пяти минут.', 'a': ['Break it into small steps and start with five minutes.', 'Break it down into small steps and just start with 5 minutes.', 'Break it into small steps and start with just five minutes.'], 'rule': L7, 'why': 'Совет — повелительное: глагол в начале'},
        {'kind': 'translate', 'ru': 'Друг: «ok, I\'ll try» Ответьте: Удачи! Напиши мне, когда закончишь.', 'a': ["Good luck! Text me when you're done.", 'Good luck! Message me when you finish.', "Good luck! Let me know when you're done."], 'rule': L7, 'why': 'После when — Present, не will'},
        {'kind': 'translate', 'ru': 'Друг: «done!! that was easier than I thought» Ответьте: Отлично! Видишь, начать — самое трудное.', 'a': ['Great! See, starting is the hardest part.', 'Awesome! You see, getting started is the hardest part.', 'Great! See? Starting is the hardest part.'], 'rule': L7, 'why': 'starting — -ing как подлежащее'},
    ]},
    {'id': 'p3-d7-g44', 'type': 'write', 'title': 'Своя речь: что я откладываю', 'minutes': 6, 'optional': True,
     'prompt': 'Напишите 4–6 предложений: какие рабочие задачи вы обычно откладываете, почему (по тексту — это про чувства) и что вам помогает начать. Используйте put off, avoid, break into steps и хотя бы один Present Perfect (I\'ve put off… for…).',
     'hint': 'Подсказка: I usually put off… because… / I\'ve been putting off… for… / What helps me is…', 'minWords': 40},
]

for d in p['days']:
    n = d['day']
    if n < 4:
        continue
    for sec in ('general', 'ux'):
        for t in d.get(sec, []):
            if t['type'] == 'shadow':
                continue
            if t['id'] not in CORE[n]:
                t['optional'] = True
    if n == 6:
        d['title'] = 'Слабое — в новых форматах'
        d['general'] = D6_NEW + d['general']
        d['ux'] = D6_UX + d.get('ux', [])
    if n == 7:
        d['title'] = 'Свежая тема: почему мы откладываем дела'
        d['general'] = D7_NEW + d['general']

json.dump(p, open(os.path.join(R, 'pack-003o.json'), 'w'), ensure_ascii=False, indent=1)
for d in p['days'][3:]:
    core = [t for s in ('general', 'ux') for t in d.get(s, []) if not t.get('optional') and t['type'] != 'shadow']
    print(d['day'], d['title'], '— ядро', sum(t.get('minutes', 0) for t in core), 'мин,', len(core), 'заданий')
