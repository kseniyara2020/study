"""Медиа (3 статьи + выпуск подкаста) и диалоги д2–д7 для pack-003 (18.11.2026, по просьбе пользователя).
python3 tools/content/media4.py packs/IN.json packs/OUT.json NEW_ID
Правильный вариант в вопросах пишется первым — порядок перемешивается детерминированно."""
import json, sys, random
R = random.Random(18)

def ch(q, opts, explain, **kw):
    order = list(range(len(opts))); R.shuffle(order)
    it = {"q": q, "options": [opts[i] for i in order], "a": order.index(0), "explain": explain}
    it.update(kw); return it

def tr(ru, a): return {"kind": "translate", "ru": ru, "a": a}

VOCAB = [
 # bottom sheets
 ("a17", "dismiss", "закрыть, убрать (окно, шторку)", "Users couldn't find a way to dismiss the sheet.", "B2"),
 ("a18", "overlay", "оверлей, слой поверх экрана", "A bottom sheet is a partial overlay.", "C1"),
 ("a19", "preserve the context", "сохранить контекст", "The sheet preserves the context of the page behind it.", "B2"),
 ("a20", "obscure", "закрывать, заслонять", "Don't let the sheet obscure the content users need.", "C1"),
 ("a21", "stack", "накладывать друг на друга, стопка", "Avoid stacking several sheets on top of each other.", "B2"),
 ("a22", "transient", "временный, мимолётный", "Sheets are transient, not places to spend time in.", "C1"),
 ("a23", "overlook", "не заметить, упустить", "Many users overlook the grab handle.", "B2"),
 ("a24", "disoriented", "сбитый с толку, потерявший ориентацию", "If Back doesn't work, users feel disoriented.", "C1"),
 # error messages
 ("a25", "an afterthought", "то, о чём думают в последнюю очередь", "Error handling is often an afterthought.", "C1"),
 ("a26", "redundant", "дублирующий, избыточный", "Use redundant indicators: colour, an icon and text.", "C1"),
 ("a27", "premature", "преждевременный", "A premature error message appears before the user has finished.", "C1"),
 ("a28", "jargon", "профессиональный жаргон", "Write in plain language, without technical jargon.", "B2"),
 ("a29", "concise", "краткий, ёмкий", "Keep the message concise and precise.", "B2"),
 ("a30", "blame someone", "винить кого-то", "A good error message doesn't blame the user.", "B1"),
 ("a31", "safeguard against", "защищать от, страховать от", "Safeguard against likely mistakes.", "C1"),
 ("a32", "undermine", "подрывать, ослаблять", "Too much technical detail can undermine understanding.", "C1"),
 # never too late
 ("a33", "receptive (to)", "восприимчивый (к)", "Young children are very receptive to new sounds.", "C1"),
 ("a34", "acquire", "приобрести, усвоить (навык, язык)", "Children acquire a native accent more easily.", "B2"),
 ("a35", "refine", "совершенствовать, оттачивать", "Adults can keep refining their grammar.", "C1"),
 ("a36", "proficiency", "уровень владения", "Pronunciation is only one part of proficiency.", "C1"),
 ("a37", "inhibition", "скованность, зажатость", "Anxiety and inhibition can slow progress.", "C2"),
 ("a38", "aptitude", "способности, склонность", "She has a natural aptitude for languages.", "C1"),
 ("a39", "deliberate", "осознанный, намеренный", "Adults learn in a more deliberate way.", "B2"),
 ("a40", "pronounced", "ярко выраженный", "Age differences are most pronounced in accent.", "C1"),
 # podcast
 ("a41", "implicit", "неявный, подразумеваемый", "Apps mostly teach rules in an implicit way.", "C1"),
 ("a42", "explicit", "явный, прямо объяснённый", "Adults benefit from explicit grammar teaching.", "C1"),
 ("a43", "full immersion", "полное погружение", "Children learn through full immersion.", "C1"),
 ("a44", "key finding", "главный вывод исследования", "The key finding was surprising.", "B2"),
]
VOC = [{"id": i, "en": en, "ru": ru, "ex": ex, "lvl": lvl, "tag": "media"} for i, en, ru, ex, lvl in VOCAB]

NOTE_ART = "Вопросы и задания составлены по статье своими словами; текст статьи здесь не копируется — читайте по ссылке."
MEDIA = [
 {"id": "art-bottom-sheets", "kind": "article", "topic": "ux", "title": "Bottom sheets: definition and UX guidelines",
  "source": "Nielsen Norman Group", "author": "Page Laubheimer", "published": "11.06.2023", "level": "B2", "minutes": 25,
  "url": "https://www.nngroup.com/articles/bottom-sheet/",
  "about": "Что такое нижняя шторка, чем модальная отличается от немодальной и 4 правила: поддержать «Назад», видимая кнопка «Закрыть», не накладывать шторки друг на друга, только для коротких задач. Прямо про ваши макеты — и про фразу bottom sheet, которая не вспоминалась.",
  "note": NOTE_ART,
  "tasks": [
   {"id": "m4-1", "type": "cards", "title": "Слова до чтения", "minutes": 4, "cards": ["a17", "a18", "a19", "a20", "a21", "a22", "a23", "a24"]},
   {"id": "m4-2", "type": "quiz", "title": "Понимание статьи", "minutes": 8, "items": [
     ch("What is a bottom sheet, according to the article?", ["An overlay attached to the bottom edge of a mobile screen", "A menu attached to the top edge of the screen", "A separate page with extra details"], "Шторка — оверлей, прикреплённый к нижнему краю экрана."),
     ch("Why can a sheet be better than opening a new page?", ["Part of the current screen stays visible", "It loads much faster", "It is easier to build"], "Шторка сохраняет контекст: часть экрана остаётся видна, не нужно заново ориентироваться."),
     ch("What does the article say about reachability?", ["The idea that sheets are easier to reach is mostly wrong", "The bottom of the screen is the easiest place to tap", "Everyone holds the phone with one hand"], "Автор считает миф о доступности неверным: легче всего нажимать в середине экрана."),
     ch("What is true about a modal bottom sheet?", ["Users must deal with it before using the screen behind it", "Users can still use the screen behind it", "It never has a dark background"], "Модальная шторка блокирует фон — обычно его затемняет scrim."),
     ch("Which example shows a nonmodal sheet?", ["Map details while you can still move the map", "A connection error that must be fixed first", "A second sheet with product reviews"], "Немодальная шторка — как в Google Maps: детали поверх карты, а карту можно двигать."),
     ch("Why does the article recommend a visible Close button?", ["The grab handle is easy to miss and swipes can be confusing", "Users never use gestures", "The Back button doesn't exist on phones"], "Ручку легко не заметить, а свайп вниз может открыть системную панель."),
     ch("What problem does stacking sheets create?", ["Users have to keep track of where they are", "The app becomes slower", "The sheets become too small to read"], "В стопке шторок трудно понять, где ты и что закроет кнопка."),
     ch("What are bottom sheets best for?", ["Short, quick tasks", "Long, complex content", "Replacing normal page navigation"], "Шторки — для коротких действий, не для длинного контента и не вместо страниц."),
   ]},
   {"id": "m4-3", "type": "translate", "title": "Перевод с новыми словами", "minutes": 5, "items": [
     tr("Пользователь не может закрыть эту шторку.", ["The user can't dismiss this sheet.", "The user can't dismiss this bottom sheet.", "Users can't dismiss this sheet.", "The user cannot dismiss this bottom sheet."]),
     tr("Шторка закрывает важную информацию.", ["The sheet obscures important information.", "The bottom sheet obscures important information.", "The sheet hides important information."]),
     tr("Не накладывайте шторки друг на друга.", ["Don't stack bottom sheets.", "Don't stack sheets on top of each other.", "Do not stack bottom sheets.", "Don't stack bottom sheets on top of each other."]),
     tr("Многие пользователи не замечают ручку.", ["Many users overlook the grab handle.", "A lot of users overlook the grab handle.", "Many users don't notice the grab handle."]),
     tr("Шторка сохраняет контекст страницы.", ["The sheet preserves the context of the page.", "A bottom sheet preserves the page context.", "The bottom sheet keeps the context of the page."]),
   ]},
   {"id": "m4-4", "type": "write", "title": "Пересказ и мнение", "minutes": 8,
    "prompt": "Перескажите статью своими словами (3–4 предложения; можно надиктовать) и ответьте: где в мобильном интерфейсе шторка уместна, а где лучше отдельная страница? Почему? Используйте минимум 3 слова из статьи.",
    "hint": "The article is about… / A bottom sheet works well when… / I'd use a separate page when…", "minWords": 70},
  ]},
 {"id": "art-error-messages", "kind": "article", "topic": "ux", "title": "Error-message guidelines",
  "source": "Nielsen Norman Group", "author": "Tim Neusesser, Evan Sunwall", "published": "14.05.2023", "level": "B2", "minutes": 25,
  "url": "https://www.nngroup.com/articles/error-message-guidelines/",
  "about": "12 правил для сообщений об ошибках в трёх группах: заметность (рядом с полем, не только цвет, не показывать раньше времени), текст (понятный язык, кратко, совет, не винить пользователя), экономия усилий (сохранить ввод, предложить исправление). Много лексики для UX-текстов и ревью.",
  "note": NOTE_ART,
  "tasks": [
   {"id": "m5-1", "type": "cards", "title": "Слова до чтения", "minutes": 4, "cards": ["a25", "a26", "a27", "a28", "a29", "a30", "a31", "a32"]},
   {"id": "m5-2", "type": "quiz", "title": "Понимание статьи", "minutes": 8, "items": [
     ch("Why do error messages often get little attention?", ["Teams focus on the ideal user path", "Users rarely make mistakes", "They are hard to translate"], "Команды думают об «идеальном пути», и ошибки остаются на потом — afterthought."),
     ch("Where should an error message appear?", ["Close to the element that caused it", "Always at the top of the page", "Always in a pop-up window"], "Сообщение — рядом с полем, которое нужно исправить."),
     ch("Why shouldn't designers rely on colour alone?", ["Many people have colour-vision deficiencies", "Red looks too aggressive", "Colours look different on every phone"], "Многие плохо различают цвета — нужны дублирующие признаки: иконка, текст, рамка."),
     ch("When is a modal dialog appropriate?", ["For serious errors that need action", "For any small warning", "For possible delivery delays"], "Модальное окно — только для серьёзных ошибок; мелочи — подписью, тостом, баннером."),
     ch("What is wrong with showing an error as soon as an empty field loses focus?", ["The user may just be exploring the form", "It makes the page slower", "It hides the field label"], "Это преждевременная ошибка: человек ещё ничего не сделал неправильно."),
     ch("Which message follows the guidelines?", ["One that explains the problem and how to fix it", "\"An error occurred.\"", "A funny pun with no explanation"], "Хорошее сообщение точно называет проблему и подсказывает, что делать."),
     ch("Which words does the article suggest avoiding?", ["Invalid, illegal, incorrect", "Please, sorry, thanks", "Save, edit, try again"], "Слова invalid / illegal / incorrect звучат как обвинение пользователя."),
     ch("What does \"preserve the user's input\" mean?", ["Keep what the user typed so they don't have to retype it", "Save the user's password automatically", "Send the input to customer support"], "Сохранить введённое, чтобы человек исправил, а не набирал заново."),
   ]},
   {"id": "m5-3", "type": "translate", "title": "Перевод с новыми словами", "minutes": 5, "items": [
     tr("Об ошибках часто думают в последнюю очередь.", ["Errors are often an afterthought.", "Error messages are often an afterthought.", "Error handling is often an afterthought."]),
     tr("Не показывайте ошибку раньше времени.", ["Don't show the error prematurely.", "Don't show premature error messages.", "Do not show errors too early.", "Don't show an error too early."]),
     tr("Пишите кратко и без жаргона.", ["Write concisely and avoid jargon.", "Be concise and don't use jargon.", "Write concisely, without jargon.", "Keep it concise and avoid jargon."]),
     tr("Не вините пользователя.", ["Don't blame the user.", "Do not blame the user.", "Don't blame users."]),
     tr("Сохраните то, что ввёл пользователь.", ["Preserve the user's input.", "Keep what the user has entered.", "Save what the user typed.", "Keep the user's input."]),
   ]},
   {"id": "m5-4", "type": "write", "title": "Перепишите сообщение об ошибке", "minutes": 8,
    "prompt": "Найдите в любом приложении или сайте одно неудачное сообщение об ошибке. Опишите его по-английски и перепишите по правилам статьи: где его показать, что написать, как помочь исправить. Используйте минимум 3 слова из статьи.",
    "hint": "The message says… / It's not clear because… / I'd show it next to… / A better message: …", "minWords": 60},
  ]},
 {"id": "art-never-too-late", "kind": "article", "topic": "general", "title": "It's never too late to learn a language",
  "source": "The Conversation (перепечатка Cobb County Courier)", "author": "Karen Stollznow", "published": "27.02.2026", "level": "B2–C1", "minutes": 25,
  "url": "https://cobbcountycourier.com/2026/02/its-never-too-late-to-learn-a-language-adults-and-kids-bring-different-strengths-to-the-task/",
  "about": "Лингвист объясняет, чем взрослые и дети отличаются в изучении языка: у детей — акцент и погружение, у взрослых — осознанность, правила, стратегии. Почему страх ошибок тормозит прогресс сильнее возраста. Тема прямо про вас и ваш путь B1 → B2.",
  "note": NOTE_ART,
  "tasks": [
   {"id": "m6-1", "type": "cards", "title": "Слова до чтения", "minutes": 4, "cards": ["a33", "a34", "a35", "a36", "a37", "a38", "a39", "a40"]},
   {"id": "m6-2", "type": "quiz", "title": "Понимание статьи", "minutes": 8, "items": [
     ch("What is the main message of the article?", ["People can learn a language at any age", "Only children can become fluent", "Adults should focus only on pronunciation"], "Главная мысль: способность учить язык с возрастом не «выключается»."),
     ch("Where are the effects of age strongest?", ["In accent", "In vocabulary", "In grammar"], "Сильнее всего возраст влияет на акцент."),
     ch("Why does the author mention birds?", ["They also learn their song during an early sensitive period", "They can learn several songs at once", "They learn faster when they are older"], "Птицы учат песню у взрослой птицы в ранний «чувствительный период»."),
     ch("Which of these is an adult strength?", ["Studying rules and comparing languages", "Hearing very subtle sounds", "Not worrying about mistakes"], "Взрослые учат осознанно: правила, сравнение языков, стратегии."),
     ch("In classrooms, adults often do better than children…", ["in the early stages, especially in reading and writing", "in pronunciation", "only after many years"], "На первых этапах взрослые часто обгоняют детей — особенно в чтении и письме."),
     ch("What can slow progress at any age?", ["Anxiety and fear of making mistakes", "Using a dictionary", "Learning grammar rules"], "Тревога, зажатость и негативная реакция тормозят прогресс в любом возрасте."),
     ch("What does the article say about accents?", ["People often wrongly link an accent with lower competence", "An accent shows lower intelligence", "An accent usually disappears after a year"], "Слушатели часто несправедливо связывают акцент с меньшей компетентностью."),
     ch("Who tends to reach higher fluency?", ["Learners with a strong personal connection to the language", "Learners with the highest IQ", "Learners who study only for exams"], "Дальше всех продвигаются те, у кого есть личная, эмоциональная связь с языком."),
   ]},
   {"id": "m6-3", "type": "translate", "title": "Перевод с новыми словами", "minutes": 5, "items": [
     tr("Взрослые учатся более осознанно.", ["Adults learn more deliberately.", "Adults learn in a more deliberate way.", "Adult learners are more deliberate."]),
     tr("Произношение — лишь одна часть владения языком.", ["Pronunciation is only one part of proficiency.", "Pronunciation is just one part of language proficiency.", "Pronunciation is only one part of language proficiency."]),
     tr("Страх ошибок может замедлить прогресс.", ["Fear of mistakes can slow down progress.", "Fear of making mistakes can slow your progress.", "Being afraid of mistakes can slow progress.", "The fear of making mistakes can slow down progress."]),
     tr("Я продолжаю оттачивать свою грамматику.", ["I keep refining my grammar.", "I'm still refining my grammar.", "I continue to refine my grammar.", "I continue refining my grammar."]),
     tr("У неё природные способности к языкам.", ["She has a natural aptitude for languages.", "She has an aptitude for languages.", "She has a natural aptitude for learning languages."]),
   ]},
   {"id": "m6-4", "type": "write", "title": "Статья и мой опыт", "minutes": 8,
    "prompt": "Что из статьи совпадает с вашим опытом изучения английского? Что вы будете делать иначе после неё? 4–6 предложений, минимум 3 слова из статьи.",
    "hint": "The article says that… / In my experience… / From now on, I'm going to…", "minWords": 60},
  ]},
 {"id": "pod-apps", "kind": "podcast", "topic": "general", "title": "6 Minute English: Can apps teach you a language?",
  "source": "BBC Learning English", "published": "10.09.2026", "level": "B1–B2", "minutes": 25,
  "url": "https://podcasts.apple.com/podcast/262026947?l=en",
  "about": "Выпуск от 10.09.2026: ведущие Нил и Пиппа обсуждают, могут ли приложения вроде Duolingo научить языку, чем «неявное» обучение отличается от «явного» и что показывают исследования. В подкаст-приложении найдите выпуск по названию.",
  "note": "Расшифровка выпуска мне недоступна — вопросы составлены по подробному содержанию выпуска. Если какой-то вопрос не совпадёт с услышанным, отметьте это заметкой — исправлю.",
  "tasks": [
   {"id": "m7-1", "type": "lesson", "title": "Как слушать выпуск", "minutes": 2, "body": [
     "**Перед прослушиванием** — карточки: 4 слова, без которых выпуск трудно понять.",
     "**1-й раз** — слушайте целиком, не останавливаясь, и сразу отвечайте на вопросы «Понимание выпуска». Не уверены — прослушайте ещё раз, это нормально.",
     "**2-й раз** — записывайте слова, которые разбирают ведущие (обычно их около шести).",
     "**3-й раз** — включите 30 секунд и повторяйте за ведущими вслух (shadowing)."], "examples": []},
   {"id": "m7-2", "type": "cards", "title": "Слова до прослушивания", "minutes": 3, "cards": ["a41", "a42", "a43", "a44"]},
   {"id": "m7-3", "type": "quiz", "title": "Понимание выпуска", "minutes": 8, "items": [
     ch("What is the episode mainly about?", ["Whether apps can help you learn a language", "Which language app is the cheapest", "How children learn to read"], "Тема — могут ли приложения научить языку."),
     ch("Which apps are mentioned as examples at the start?", ["Duolingo, Babbel and Busuu", "Duolingo, Netflix and Spotify", "Only Duolingo"], "В начале упоминают Duolingo, Babbel и Busuu."),
     ch("According to the episode, how do apps mostly teach?", ["Implicitly — the rules are suggested, not explained", "Explicitly — with long grammar explanations", "Only through conversations with teachers"], "Приложения в основном учат неявно: правило подразумевается, а не объясняется."),
     ch("What does \"implicit\" mean?", ["Suggested but not said directly", "Explained very clearly", "Very difficult to understand"], "implicit — подразумеваемый, не высказанный прямо."),
     ch("Why do adults need more explicit teaching, according to the expert?", ["They don't get constant exposure to the language like children", "Their memory is worse than children's", "They don't like using apps"], "Ребёнок постоянно окружён языком, а взрослый учится несколько часов в неделю."),
     ch("What would it help to copy from children, according to one speaker?", ["Full immersion", "Short lessons", "Playing games"], "Полезно повторить то, что делают дети, — полное погружение."),
     ch("In a study of Spanish speakers learning English, app users did better at…", ["written grammar tests", "listening", "speaking"], "Пользователи приложения лучше справились с письменными тестами по грамматике."),
     ch("In the same study, classroom learners improved more at…", ["listening", "written grammar tests", "spelling"], "Ученики в классе сильнее продвинулись в аудировании."),
     ch("What does the expert suggest?", ["A combination of human teaching and apps for repetition", "Using only apps", "Using only a teacher"], "Лучше сочетать живое обучение и приложения для повторения."),
     ch("Why is the research on apps limited?", ["Studies often look at one language, one app or one school", "There are no studies at all", "App companies don't allow research"], "Исследования узкие: один язык, одно приложение или одна школа."),
   ]},
   {"id": "m7-4", "type": "write", "title": "Слова выпуска", "minutes": 6,
    "prompt": "Запишите слова, которые разбирали ведущие (около шести), — к каждому пример из выпуска или свой.",
    "hint": "1. implicit — … / 2. …", "minWords": 25},
   {"id": "m7-5", "type": "write", "title": "Пересказ и мнение", "minutes": 8,
    "prompt": "Перескажите выпуск в 3–4 предложениях (можно надиктовать) и ответьте: что в вашей учёбе implicit, а что explicit? Что вам помогает больше?",
    "hint": "The episode is about… / In my studies, … is explicit because… / What helps me most is…", "minWords": 60},
  ]},
]

# ---------- диалоги д2–д7 ----------
def dlg(day, title, lines, items):
    return {"id": f"p3-d{day}-g20", "type": "dialog", "title": "Диалог: " + title, "minutes": 5,
            "lines": [{"s": s, "t": t} for s, t in lines], "items": items}
DIALOGS = {
 2: ("новый коллега", [
   ("Anna", "Hi Tom, welcome to the team! What are you working on this week?"),
   ("Tom", "Thanks! I'm working on the search page. Do you know who designed the filters?"),
   ("Anna", "I did, actually. What do you think of them?"),
   ("Tom", "They look great. But who decided to hide the sort button?"),
   ("Anna", "The product manager did. Users told us it was confusing. Could you tell me what the problem is?"),
   ("Tom", "Nothing serious. I just wonder how users will find it on mobile."),
   ("Anna", "Good question. Let's ask the research team what they found."),
  ], [
   ("What is Tom working on this week?", ["The search page", "The filters page", "The mobile menu"], "I'm working on the search page.", "What are you working on? — предлог on в конце вопроса"),
   ("Who designed the filters?", ["Anna", "The product manager", "The research team"], "Who designed the filters? — I did (Anna).", "Who designed…? — вопрос к подлежащему, без did"),
   ("Who decided to hide the sort button?", ["The product manager", "Anna", "Tom"], "The product manager did.", "Who decided…? — к подлежащему; ответ: The product manager did"),
   ("What is Tom not sure about?", ["How users will find the sort button on mobile", "Whether the filters look good", "Who will test the search page"], "I just wonder how users will find it on mobile.", "I wonder how users will find… — после I wonder прямой порядок"),
  ]),
 3: ("запуск откладывается", [
   ("PM", "Bad news, I'm afraid. The client has put off the launch until March."),
   ("Designer", "Oh no. Have they called off the whole project?"),
   ("PM", "No, just the launch. They want us to figure out why users drop out at the payment step."),
   ("Designer", "I can look into it this week. I'll set up a few interviews."),
   ("PM", "Great. Can you bring it up at Friday's meeting?"),
   ("Designer", "Sure. I'll go over the results with the team first."),
  ], [
   ("What has the client done?", ["Postponed the launch until March", "Cancelled the whole project", "Moved the launch to February"], "The client has put off the launch until March.", "put off = отложить; call off = отменить"),
   ("What do they want the team to find out?", ["Why users leave at the payment step", "Why users leave at the sign-up step", "How much the payment step costs"], "…figure out why users drop out at the payment step.", "figure out = разобраться; drop out = выбыть, бросить"),
   ("What will the designer do this week?", ["Set up a few interviews", "Redesign the payment step", "Call the client"], "I'll set up a few interviews.", "set up = организовать"),
   ("When will they discuss it with the PM?", ["At Friday's meeting", "At Monday's meeting", "In March"], "Can you bring it up at Friday's meeting?", "bring up = поднять тему"),
  ]),
 4: ("клиенту не нравятся цвета", [
   ("Lead", "Hi Kate, are you busy right now?"),
   ("Kate", "A little. I'm finishing the icons for the settings page. Why?"),
   ("Lead", "The client doesn't like the new colours. They say the buttons aren't clear enough."),
   ("Kate", "Really? Do they want a darker blue?"),
   ("Lead", "They don't know yet. They're testing two versions with their users this week."),
   ("Kate", "OK. I usually don't change colours before the test results, so let's wait."),
  ], [
   ("What is Kate doing right now?", ["Finishing the icons for the settings page", "Testing two versions", "Changing the colours"], "I'm finishing the icons for the settings page.", "Сейчас, процесс → am + -ing"),
   ("What doesn't the client like?", ["The new colours", "The new icons", "The settings page"], "The client doesn't like the new colours.", "the client = he/she → doesn't like"),
   ("What is the client doing this week?", ["Testing two versions with users", "Choosing a darker blue", "Redesigning the buttons"], "They're testing two versions with their users this week.", "Временное действие на этой неделе → are testing"),
   ("What does Kate usually do?", ["She waits for test results before changing colours", "She changes colours straight away", "She asks the client to choose"], "I usually don't change colours before the test results.", "usually — привычка → Present Simple: don't change"),
  ]),
 5: ("опыт на собеседовании", [
   ("Interviewer", "Have you ever worked on a banking app?"),
   ("Candidate", "Yes, I have. I worked on one at my previous company in 2024."),
   ("Interviewer", "What did you do there?"),
   ("Candidate", "I redesigned the payments flow. We launched it last spring."),
   ("Interviewer", "And what have you done since then?"),
   ("Candidate", "I've joined a logistics startup. I've designed two dashboards so far, and I've learned a lot about data tables."),
  ], [
   ("When did the candidate work on a banking app?", ["In 2024", "In 2023", "Last month"], "I worked on one at my previous company in 2024.", "Есть время в прошлом (in 2024) → Past Simple: worked"),
   ("What did she redesign?", ["The payments flow", "A dashboard", "The onboarding"], "I redesigned the payments flow.", "Законченное действие в прошлом → redesigned"),
   ("When did they launch it?", ["Last spring", "Last summer", "Last week"], "We launched it last spring.", "last spring → Past Simple"),
   ("How many dashboards has she designed so far?", ["Two", "Three", "One"], "I've designed two dashboards so far.", "so far — до сих пор → Present Perfect: have designed"),
  ]),
 6: ("как перестать работать допоздна", [
   ("Mia", "You used to work late every day. What changed?"),
   ("Leo", "I got used to planning my week on Monday. It made a big difference."),
   ("Mia", "I wish I had started doing that earlier. I always make a list, but I never do the hardest task first."),
   ("Leo", "Try it tomorrow. Do the hardest task in the morning, and make decisions after lunch."),
   ("Mia", "Good idea. I'll give it a go."),
  ], [
   ("What did Leo use to do?", ["Work late every day", "Plan his week on Monday", "Make a list every morning"], "You used to work late every day.", "used to + глагол — раньше, теперь нет"),
   ("What helped Leo?", ["Planning his week on Monday", "Working late", "Doing easy tasks first"], "I got used to planning my week on Monday.", "get used to + -ing — привыкнуть"),
   ("What does Mia regret?", ["Not starting to plan earlier", "Making lists", "Working late"], "I wish I had started doing that earlier.", "wish + Past Perfect — сожаление о прошлом"),
   ("What does Leo advise?", ["Do the hardest task in the morning", "Make decisions in the morning", "Make a list after lunch"], "Do the hardest task in the morning, and make decisions after lunch.", "do a task, make a decision"),
  ]),
 7: ("итоги интервью", [
   ("Researcher", "How did the interviews go?"),
   ("Designer", "Really well. We've talked to eight users so far. Most of them don't use the filters."),
   ("Researcher", "Why not? What did they say?"),
   ("Designer", "They didn't notice them. The button is too small, and it's hidden at the bottom."),
   ("Researcher", "Have you shared this with the product manager?"),
   ("Designer", "Not yet. I'm writing the summary now — I'll send it this afternoon."),
  ], [
   ("How many users have they talked to so far?", ["Eight", "Six", "Ten"], "We've talked to eight users so far.", "so far → Present Perfect"),
   ("What do most users not use?", ["The filters", "The search", "The sort button"], "Most of them don't use the filters.", "Most of them → они → don't use"),
   ("Why don't they use it?", ["They didn't notice it", "They don't need it", "It's too slow"], "They didn't notice them.", "Рассказ о том, что было → didn't notice"),
   ("When will the designer send the summary?", ["This afternoon", "Tomorrow morning", "Next week"], "I'll send it this afternoon.", "Решение/обещание → will send"),
  ]),
}

RULES = {6: ['p2-d2-g1', 'p2-d2-g1', 'p2-d4-g1', 'p2-d1-g1'], 7: ['p3-d5-g1', 'p3-d4-g1', 'p3-d5-g1', 'p3-d4-g1']}
src, dst, nid = sys.argv[1:4]
P = json.load(open(src))
have = {v['id'] for v in P.get('vocab', [])}
P.setdefault('vocab', []).extend(v for v in VOC if v['id'] not in have)
P['media'] = [m for m in P.get('media', []) if m['id'] not in {x['id'] for x in MEDIA}] + MEDIA
for day, (title, lines, qs) in DIALOGS.items():
    g = P['days'][day - 1]['general']
    rule = next((t['id'] for t in g if t['type'] == 'lesson'), None)
    items = []
    for k, (q, opts, ex, why) in enumerate(qs):
        it = ch(q, opts, ex, why=why)
        it['rule'] = RULES.get(day, [rule] * 4)[k]
        items.append(it)
    task = dlg(day, title, lines, items)
    g[:] = [t for t in g if t['id'] != task['id']]
    pos = next((i + 1 for i, t in enumerate(g) if 'слух' in t['title'].lower()), 2)
    g.insert(pos, task)
P['replaces'] = sorted(set((P.get('replaces') or []) + [P['id']])); P['id'] = nid
json.dump(P, open(dst, 'w'), ensure_ascii=False, indent=1)
print('OK', nid)
