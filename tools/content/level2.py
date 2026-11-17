#!/usr/bin/env python3
"""Генератор теста level-v2 (контрольная 27.11–11.12.2026): python3 tools/content/level2.py
Все вопросы новые (не из level-v1). Правильный вариант пишется первым, порядок вариантов перемешивается детерминированно."""
import json, os, random

R = random.Random(7)
def item(q, opts, band, **extra):
    order = list(range(len(opts))); R.shuffle(order)
    it = dict(extra)
    if q: it['q'] = q
    it.update(options=[opts[i] for i in order], a=order.index(0), band=band)
    return it

grammar = [
    # A2
    item("___ your manager in the office today?", ["Is", "Does", "Do"], "A2"),
    item("My colleague ___ coffee — she only drinks tea.", ["doesn't drink", "don't drink", "isn't drink"], "A2"),
    item("Where ___ you go on holiday last summer?", ["did", "were", "do"], "A2"),
    item("He ___ in Berlin, but he often travels to Paris for work.", ["lives", "live", "is live"], "A2"),
    item("Can I ask you ___ question?", ["a", "an", "the"], "A2"),
    # B1
    item("I've never ___ a mistake like this before.", ["made", "done", "did"], "B1"),
    item("Could you tell me what time ___?", ["the meeting starts", "does the meeting start", "starts the meeting"], "B1"),
    item("I ___ this app for two years, and I still like it.", ["have used", "use", "am using"], "B1"),
    item("She decided ___ the job in London.", ["to take", "taking", "take"], "B1"),
    item("Choose the correct question.", ["Who wrote this report?", "Who did wrote this report?", "Who this report wrote?"], "B1"),
    # B2
    item("I'm not used to ___ so early.", ["getting up", "get up", "got up"], "B2"),
    item("Could you ___ me a favour and check these screens?", ["do", "make", "give"], "B2"),
    item("If I ___ more time, I'd learn Japanese.", ["had", "have", "would have"], "B2"),
    item("The client asked us to ___ with a cheaper solution.", ["come up", "come out", "come over"], "B2"),
    item("I wish I ___ that email — it caused a lot of problems.", ["hadn't sent", "didn't send", "wouldn't send"], "B2"),
    # C1
    item("Rarely ___ such a clear presentation from a junior designer.", ["have I seen", "I have seen", "I saw"], "C1"),
    item("___ the budget been approved earlier, we could have started in May.", ["Had", "If", "Has"], "C1"),
    item("We need to ___ the risks before the launch.", ["mitigate", "militate", "mediate"], "C1"),
    item("No sooner had we launched the update ___ users started reporting bugs.", ["than", "when", "then"], "C1"),
    item("She is said ___ the company's original design system.", ["to have created", "to create", "having created"], "C1"),
]

reading = [
    {"title": "Текст 1 · Сообщение команде",
     "passage": "Hi all,\n\nA quick update about the design review on Thursday. We're moving it from 10 a.m. to 2 p.m., because the product manager has a call with a client in the morning.\n\nThe review will be in Room 4, not online, so please come to the office if you can. If you can't, add your comments to the shared document by Wednesday evening.\n\nPlease bring printed copies of your two best screens — we'll put them on the wall and vote for the strongest ideas.\n\nThanks,\nDaniel",
     "items": [
         item("What time is the review now?", ["2 p.m.", "10 a.m.", "Wednesday evening"], "A2"),
         item("Why has the time changed?", ["The product manager has a call with a client", "Room 4 is busy in the morning", "Daniel is away on Thursday morning"], "A2"),
         item("What should people who can't come do?", ["Add comments to the shared document by Wednesday evening", "Join the review online", "Send their printed screens to Daniel"], "B1"),
         item("What will happen to the printed screens?", ["They'll go on the wall, and people will vote", "They'll be sent to the client", "The product manager will choose the best one"], "B1"),
     ]},
    {"title": "Текст 2 · Статья о дизайн-ревью",
     "passage": "For years, the design team at a mid-sized travel company presented finished work to managers once a month. The meetings were long, and feedback often arrived too late: by the time someone pointed out a problem, developers had already started building.\n\nLast spring, the team tried something different. Instead of monthly presentations, they began sharing rough sketches in short weekly sessions with developers and support staff. Nobody was allowed to say whether they liked a design; people could only ask questions or describe what a user might struggle with.\n\nAt first, some designers felt uncomfortable showing unfinished work. \"It felt like going out before you're properly dressed,\" one of them admitted. But after a couple of months, the number of late changes had fallen by almost half, and support staff were spotting problems that designers had missed, because they spoke to customers every day.\n\nThe team's lead says the biggest benefit was not speed. \"People stopped defending their designs and started discussing the problem,\" she explains.",
     "items": [
         item("What was the main problem with the monthly presentations?", ["Feedback came after development had started", "They were too short", "Managers rarely came to them"], "B1"),
         item("In the weekly sessions, people were not allowed to…", ["say whether they liked a design", "ask questions", "describe what users might struggle with"], "B1"),
         item("Why were support staff especially useful?", ["They talked to customers every day", "They had design training", "They worked closely with managers"], "B2"),
         item("According to the team lead, the most important change was that…", ["people focused on the problem instead of defending their work", "the team started working faster", "designers felt comfortable showing sketches"], "B2"),
     ]},
    {"title": "Текст 3 · Статья о метриках",
     "passage": "Few things are as tempting to a manager as a number that goes up. Tickets closed, screens delivered, hours logged — each promises a clear picture of who is working hard. Yet economists have long warned about what is known as Goodhart's law: once a measure becomes a target, it stops being a good measure.\n\nThe problem is not that people cheat, although some do. It is that any single number captures only part of the job, and people naturally shift their effort towards the part that is counted. A designer judged on the number of screens delivered has little reason to spend a day talking to users, even if that conversation would save weeks of rework.\n\nThis does not mean that measurement is useless. Teams that use several indicators together, and treat them as starting points for conversation rather than verdicts, tend to avoid the worst distortions. What matters, researchers suggest, is less what is measured than how the results are used.\n\nSome critics go further, arguing that the most valuable work — mentoring a colleague, noticing a problem before it appears — is precisely the kind that resists measurement. Their point is not to abandon numbers, but to remember what they leave out.",
     "items": [
         item("What does Goodhart's law say, as described in the text?", ["A measure loses its value when it becomes a target", "Numbers always improve over time", "Managers should never set targets"], "B2"),
         item("According to the text, why does a single number cause problems?", ["People focus their effort on what is counted", "Most people cheat to improve it", "It is difficult to calculate correctly"], "B2"),
         item("The writer suggests that measurement works better when…", ["results start a discussion rather than act as a final judgement", "a team uses only one clear indicator", "results are not shared with the team"], "C1"),
         item("What is the critics' main point?", ["Some of the most valuable work is hard to measure", "Teams should stop using numbers", "Mentoring matters more than design work"], "C1"),
     ]},
]

listening = [
    {"title": "Часть 1 · Короткие фразы", "items": [
        item("When does the speaker want to meet?", ["At half past four", "At three", "At quarter past four"], "A2",
             say="Sorry, I can't make it at three. Can we meet at half past four instead?"),
        item("What does the client want?", ["The blue version with a bigger logo", "The blue version with a smaller logo", "A new colour with a bigger logo"], "A2",
             say="The client liked the blue version, but she wants the logo a little bigger."),
        item("Why hasn't the report been sent?", ["The speaker is waiting for numbers from finance", "Finance hasn't approved it yet", "The speaker forgot about it"], "B1",
             say="I was going to send the report today, but I'm still waiting for the numbers from finance."),
        item("What does the speaker think of the new search?", ["It's fast, but the filters need work", "It's fast, and the filters are good", "It's slow, but the filters are good"], "B1",
             say="If you haven't tried the new search yet, you really should — it's much faster, though the filters still need some work."),
    ]},
    {"title": "Часть 2 · Разработчик и дизайнер",
     "lines": [
         {"s": "Developer", "t": "Hi, I've started on the settings screen. Quick question about the toggle states."},
         {"s": "Designer", "t": "Sure. Which part is unclear?"},
         {"s": "Developer", "t": "In the file there's an 'on' and an 'off' state, but nothing for when the setting is loading. What should people see while we wait for the server?"},
         {"s": "Designer", "t": "Good catch — I didn't design that. For now, let's show the toggle in grey and disable it. I'll add a proper loading state to the file by tomorrow morning."},
         {"s": "Developer", "t": "Great. And on smaller phones, some labels wrap onto two lines. Is that okay?"},
         {"s": "Designer", "t": "Two lines is fine, but not three. If a label needs three lines, let me know and I'll shorten the text."},
     ],
     "items": [
         item("What is the developer working on?", ["The settings screen", "The login screen", "The search screen"], "B1"),
         item("What was missing from the design file?", ["A loading state", "The 'off' state", "The labels for small phones"], "B1"),
         item("What will people see while the setting is loading, for now?", ["A grey toggle that doesn't work", "No toggle at all", "A short loading message"], "B2"),
         item("What does the designer say about long labels?", ["Two lines is the maximum", "Labels must fit on one line", "Three lines is fine on small phones"], "B2"),
     ]},
    {"title": "Часть 3 · Выступление об интервью",
     "lines": [
         {"s": "Speaker", "t": "Thanks for coming. I'd like to share one lesson from our user interviews this quarter."},
         {"s": "Speaker", "t": "We spoke to twenty small business owners about how they send invoices. Almost all of them said the process was easy. However, when we asked them to show us how they actually did it, most of them used two or three different tools and copied numbers by hand."},
         {"s": "Speaker", "t": "In other words, what people say and what people do are often quite different — not because they're lying, but because they've got used to the extra steps and no longer notice them."},
         {"s": "Speaker", "t": "So my suggestion for next quarter is simple: in every interview, let's spend at least half the time watching people complete a real task, rather than asking them to describe it. We'll get fewer quotes for our slides, but far more useful findings."},
     ],
     "items": [
         item("What did most business owners say about sending invoices?", ["It was easy", "It was difficult", "It took too long"], "B2"),
         item("What did the researchers notice when they watched?", ["People used several tools and copied numbers by hand", "People made many mistakes in the numbers", "People refused to show their process"], "B2"),
         item("According to the speaker, why do people describe the process inaccurately?", ["They no longer notice the extra steps", "They want to impress the researchers", "They don't understand the questions"], "C1"),
         item("What trade-off does the speaker accept?", ["Fewer quotes for presentations, but more useful findings", "Fewer interviews, but longer ones", "Less time watching, but more participants"], "C1"),
     ]},
]

test = {
    "type": "level-test", "id": "level-v2", "version": 2,
    "title": "Проверка уровня · версия 2", "created": "2026-11-17",
    "window": {"from": "2026-11-27", "to": "2026-12-11"},
    "skills": {
        "grammar": {"title": "Грамматика и лексика", "minutes": 12,
                    "about": "20 вопросов от A2 до C1, сложность растёт. Если не знаете ответа, не угадывайте наугад — выбирайте, только если есть мысль.",
                    "parts": [{"title": "Выберите правильный вариант", "items": grammar}]},
        "reading": {"title": "Чтение", "minutes": 15,
                    "about": "3 текста разной сложности, по 4 вопроса к каждому. Текст можно перечитывать сколько угодно.",
                    "parts": reading},
        "listening": {"title": "Аудирование", "minutes": 12,
                      "about": "3 части: короткие фразы, диалог, выступление. Слушайте сколько угодно раз; варианты ответа отличаются одной деталью — слушайте внимательно.",
                      "parts": listening},
        "writing": {"title": "Письмо", "minutes": 35,
                    "about": "2 задания. Оценивает Claude по критериям CEFR: содержание, достижение цели, организация текста, язык. Без переводчика и проверки орфографии — так оценка будет честной. Результат придёт после экспорта.",
                    "parts": [
                        {"title": "Задание 1 · Письмо менеджеру (B1)",
                         "prompt": "You won't be able to finish the designs for a new feature by the deadline on Friday. Write an email to your project manager (80–100 words):\n• explain why the work is taking longer;\n• say what is already done;\n• suggest a new date and offer something that could help.",
                         "minWords": 70},
                        {"title": "Задание 2 · Эссе-мнение (B2)",
                         "prompt": "Some people say that AI tools will soon make junior designers unnecessary. Do you agree? Write an essay (140–190 words) giving your opinion. Support it with reasons and examples.",
                         "minWords": 120},
                    ]},
        "speaking": {"title": "Говорение", "minutes": 15, "mode": "chat",
                     "about": "Говорение проходит голосом в чате **Speaking**: напишите там «контрольная». ≈ 12–15 минут, 3 части, как в Cambridge и IELTS Speaking: вопросы о себе, рассказ по карточке, обсуждение. Ошибки по ходу не исправляются. В конце Claude даст отчёт — перенесите его в чат «Экспорт / импорт», и результат придёт сюда сам."},
    },
}

out = os.path.join(os.path.dirname(__file__), '..', '..', 'packs', 'level-v2.json')
json.dump(test, open(out, 'w'), ensure_ascii=False, indent=1)
print('OK', os.path.abspath(out))
