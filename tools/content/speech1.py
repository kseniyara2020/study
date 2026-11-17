"""Блок «Из вашей речи» (голосовой разговор 17.11): один глагол-мотор — X is (не X it's), am/is/are, -s с he/she/it.
Добавляет в pack-003 урок p3-d2-s1 (день 2) и упражнение p3-dN-s2 (дни 2–7).
python3 tools/content/speech1.py packs/IN.json packs/OUT.json NEW_ID"""
import json, sys
R = 'p3-d2-s1'
W_IT = "Подлежащее уже названо → сразу глагол: X is…, без лишнего it's (русское «X — это…»)"
W_BE = "Нет действия (прилагательное, кто/что, где) → нужен am/is/are"
W_S = "he/she/it + действие → глагол с -s; в отрицании и вопросе -s уходит в does"
FIX = [
 ("Our client it's a delivery company.", "Our client is a delivery company.", "Наш клиент — компания по доставке.", W_IT),
 ("The hardest part it's the deadline.", "The hardest part is the deadline.", "Самое сложное — это дедлайн.", W_IT),
 ("I afraid of big changes.", ["I'm afraid of big changes.", "I am afraid of big changes."], "Я боюсь больших перемен.", W_BE),
 ("Our PM don't know what he want.", "Our PM doesn't know what he wants.", "Наш PM не знает, чего хочет.", W_S + ": doesn't know, wants"),
 ("Germany it's a good country.", "Germany is a good country.", "Германия — хорошая страна.", W_IT),
 ("We ready to start.", ["We're ready to start.", "We are ready to start."], "Мы готовы начать.", W_BE),
 ("The client have a lot of documents.", "The client has a lot of documents.", "У клиента много документов.", W_S + ": have → has"),
 ("Is a dashboard for our clients.", ["It's a dashboard for our clients.", "It is a dashboard for our clients."], "Это дашборд для наших клиентов.", "У предложения должно быть подлежащее: It's a dashboard…"),
 ("This feature it's not necessary.", ["This feature isn't necessary.", "This feature is not necessary."], "Эта функция не обязательна.", W_IT),
 ("She very good at research.", ["She's very good at research.", "She is very good at research."], "Она очень хороша в исследованиях.", W_BE),
 ("It don't work on Android.", ["It doesn't work on Android.", "It does not work on Android."], "Это не работает на Android.", W_S + ": it → doesn't"),
 ("My manager it's very busy this week.", "My manager is very busy this week.", "Мой менеджер очень занят на этой неделе.", W_IT),
 ("I not sure about the layout.", ["I'm not sure about the layout.", "I am not sure about the layout."], "Я не уверена насчёт макета.", W_BE + ": not sure — прилагательное"),
 ("She work from home on Fridays.", "She works from home on Fridays.", "По пятницам она работает из дома.", W_S),
 ("The new flow it's easier to use.", "The new flow is easier to use.", "Новым сценарием пользоваться проще.", W_IT),
 ("Is very hard to read on mobile.", ["It's very hard to read on mobile.", "It is very hard to read on mobile."], "На телефоне это очень трудно читать.", "Подлежащее обязательно: It's hard to…"),
 ("He need more time.", "He needs more time.", "Ему нужно больше времени.", W_S),
 ("Everyone it's here.", "Everyone is here.", "Все здесь.", W_IT + "; everyone — единственное число → is"),
 ("The users is confused.", "The users are confused.", "Пользователи сбиты с толку.", "users — они → are"),
 ("Does she knows about it?", "Does she know about it?", "Она знает об этом?", "-s уже в does → know без -s"),
 ("The problem it's in the filters.", "The problem is in the filters.", "Проблема в фильтрах.", W_IT),
 ("The app work offline.", "The app works offline.", "Приложение работает офлайн.", W_S + ": the app = it"),
 ("Design it's important for the product.", "Design is important for the product.", "Дизайн важен для продукта.", W_IT),
 ("My team lead want a short summary.", "My team lead wants a short summary.", "Мой тимлид хочет короткое резюме.", W_S),
]
GAP = [
 ("Our client ___ a logistics company. (be)", ["is"], "Наш клиент — логистическая компания.", W_IT),
 ("He ___ to see the final version. (want)", ["wants"], "Он хочет увидеть финальную версию.", W_S),
 ("I ___ worried about the deadline. (be)", ["am", "'m"], "Я переживаю из-за дедлайна.", W_BE),
 ("She ___ know about the meeting. (не знает)", ["doesn't", "does not"], "Она не знает о встрече.", W_S + ": she → doesn't + know"),
 ("The dashboard ___ the work with documents easier. (make)", ["makes"], "Дашборд упрощает работу с документами.", W_S),
 ("___ it work on tablets? (вопрос, it + действие)", ["Does"], "Это работает на планшетах?", "work — действие, it → Does"),
 ("They ___ happy with the result. (be)", ["are", "'re"], "Они довольны результатом.", W_BE + ": they → are"),
 ("The CEO ___ design is important. (think)", ["thinks"], "Генеральный директор считает, что дизайн важен.", W_S),
 ("My job ___ very stable right now. (be, отрицание)", ["isn't", "is not"], "Моя работа сейчас не очень стабильна.", W_BE + ": isn't"),
 ("This screen ___ too many buttons. (have)", ["has"], "На этом экране слишком много кнопок.", W_S + ": have → has"),
 ("___ you ready for the demo? (be)", ["Are"], "Ты готова к демо?", W_BE + ": ready — прилагательное → Are you"),
 ("Our product ___ drivers in five countries. (help)", ["helps"], "Наш продукт помогает водителям в пяти странах.", W_S),
]
ORD = [
 ("The hardest part is the communication.", "Самое сложное — это коммуникация.", W_IT),
 ("Our client is a delivery company.", "Наш клиент — компания по доставке.", W_IT),
 ("I'm not afraid of feedback.", "Я не боюсь фидбэка.", W_BE),
 ("He doesn't know what he wants.", "Он не знает, чего хочет.", W_S),
 ("It's a tool for our drivers.", "Это инструмент для наших водителей.", "Подлежащее обязательно: It's a tool…"),
 ("She works with documents every day.", "Она каждый день работает с документами.", W_S),
]
LESSON = {"id": R, "type": "lesson", "title": "Из вашей речи: один глагол-мотор", "minutes": 4, "body": [
 "Это ошибки из вашего голосового разговора 17.11. В упражнениях вы делаете их правильно, а в живой речи они проскакивают — поэтому короткий блок каждый день до конца недели.",
 "**Логика:** у каждого подлежащего в английском есть свой глагол-«мотор» — и только один на этом месте.",
 "**1. Подлежащее уже названо → сразу глагол.** По-русски «Германия — это хорошая страна», и рука тянется написать it's. Но Germany уже подлежащее, ему нужен только глагол: **Germany is** a good country. Our client **is**… The hardest part **is**…",
 "**2. Нет действия → нужен am / is / are.** Если после подлежащего прилагательное (afraid, ready, sure, busy), «кто/что» (a designer, a dashboard) или «где» (at work) — без be мотора нет: **I'm** afraid. **It's** a dashboard. **We're** ready.",
 "**3. he / she / it + действие → -s.** He want**s**, it work**s**, the client ha**s**. В отрицании и вопросе -s переезжает в does: he **doesn't** know (не knows), **does** she know?",
 "**Проверка за секунду:** назвала подлежащее — где мотор? Есть действие → глагол (с -s для he/she/it). Нет действия → am/is/are."],
 "examples": [
  {"en": "Our client is a delivery company.", "ru": "Наш клиент — компания по доставке."},
  {"en": "The hardest part is the communication.", "ru": "Самое сложное — это коммуникация."},
  {"en": "I'm afraid of big changes.", "ru": "Я боюсь больших перемен."},
  {"en": "It's a dashboard for our clients.", "ru": "Это дашборд для наших клиентов."},
  {"en": "Our PM doesn't know what he wants.", "ru": "Наш PM не знает, чего хочет."},
  {"en": "The client has a lot of documents.", "ru": "У клиента много документов."}]}
def items(k):
    out = []
    for q, a, ru, w in FIX[4*k:4*k+4]:
        out.append({"kind": "fix", "q": q, "a": a if isinstance(a, list) else [a], "explain": ru, "rule": R, "why": w})
    for q, a, ru, w in GAP[2*k:2*k+2]:
        out.append({"kind": "gap", "q": q, "a": a, "explain": ru, "rule": R, "why": w})
    for en, ru, w in [ORD[(2*k) % 6], ORD[(2*k+1) % 6]]:
        out.append({"kind": "order", "en": en, "ru": ru, "alt": [], "rule": R, "why": w})
    return out
src, dst, nid = sys.argv[1:4]
P = json.load(open(src))
for k, d in enumerate(P['days'][1:7]):
    g = d['general']
    pos = next((i for i, t in enumerate(g) if t['type'] == 'write'), len(g))
    block = [{"id": f"p3-d{k+2}-s2", "type": "mix", "title": "Из вашей речи: глагол-мотор", "minutes": 4, "items": items(k)}]
    if k == 0: block.insert(0, LESSON)
    g[pos:pos] = block
P['replaces'] = sorted(set((P.get('replaces') or []) + [P['id']])); P['id'] = nid
json.dump(P, open(dst, 'w'), ensure_ascii=False, indent=1)
