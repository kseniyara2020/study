"""Блок «Из вашей речи: to или -ing» (разговор 17.11, второй): урок p3-d3-s3 (день 3), упражнение p3-dN-s4 (дни 3–7).
python3 tools/content/speech2.py packs/IN.json packs/OUT.json NEW_ID"""
import json, sys
R = 'p3-d3-s3'
TO = "want / need / decide / plan / try / would like → to + глагол (цель, действие впереди)"
ING = "после enjoy / finish / keep / stop / mind и после предлога (for, in, at, about, to в look forward to) → -ing"
BE = "be + -ing — процесс сейчас: I'm working, I'm continuing (не I'm work / I'm continue)"
WHAT = "Действие в роли «что» (после is, в начале фразы) → -ing: The hardest part is meeting…"
S = "he/she/it + действие → -s; в отрицании -s уходит в doesn't"
PL = "things / users / they — множественное → глагол без -s"
FIX = [
 ("I want ask you a question.", ["I want to ask you a question."], "Я хочу задать вам вопрос.", TO),
 ("I'm continue work on the dashboard.", ["I'm continuing to work on the dashboard.", "I'm continuing working on the dashboard.", "I continue working on the dashboard.", "I continue to work on the dashboard.", "I'm still working on the dashboard."], "Я продолжаю работать над дашбордом.", BE + "; continue + to / -ing"),
 ("It scare me.", ["It scares me."], "Меня это пугает.", S),
 ("I need finish the layout today.", ["I need to finish the layout today."], "Мне нужно закончить макет сегодня.", TO),
 ("Thanks for help me.", ["Thanks for helping me.", "Thank you for helping me."], "Спасибо, что помогли мне.", ING),
 ("This dashboard don't have filters.", ["This dashboard doesn't have filters.", "This dashboard does not have filters."], "В этом дашборде нет фильтров.", S),
 ("She enjoys to work with clients.", ["She enjoys working with clients."], "Ей нравится работать с клиентами.", ING),
 ("Tell me how don't forget new words.", ["Tell me how not to forget new words."], "Подскажите, как не забывать новые слова.", "«как не…» → how not to + глагол: not стоит перед to"),
 ("The things that worries me most are deadlines.", ["The things that worry me most are deadlines."], "Больше всего меня беспокоят дедлайны.", PL),
 ("We decided make it responsive.", ["We decided to make it responsive."], "Мы решили сделать его адаптивным.", TO),
 ("He just don't answer.", ["He just doesn't answer.", "He just does not answer."], "Он просто не отвечает.", S),
 ("I'm interested in learn UX writing.", ["I'm interested in learning UX writing."], "Мне интересно изучать UX-тексты.", ING + ": in learning"),
 ("I'm look forward to the demo.", ["I'm looking forward to the demo."], "Жду не дождусь демо.", BE),
 ("My PM want to see the flow.", ["My PM wants to see the flow."], "Мой PM хочет увидеть сценарий.", S),
 ("I finished to design the main screen.", ["I finished designing the main screen."], "Я закончила дизайн главного экрана.", ING),
]
GAP = [
 ("The hardest part is ___ deadlines. (meet)", ["meeting"], "Самое сложное — укладываться в сроки.", WHAT),
 ("I'd like ___ you a question. (ask)", ["to ask"], "Я бы хотела задать вам вопрос.", TO),
 ("Keep ___, you're doing great. (go)", ["going"], "Продолжай, у тебя отлично получается.", ING),
 ("She ___ me with every review. (help)", ["helps"], "Она помогает мне с каждым ревью.", S),
 ("I'm trying ___ the layout simpler. (make)", ["to make"], "Я пытаюсь сделать макет проще.", TO),
 ("Stop ___ about mistakes and just speak. (worry)", ["worrying"], "Хватит переживать из-за ошибок — просто говори.", ING),
 ("What ___ you most? (worry, it)", ["worries"], "Что вас больше всего беспокоит?", "What — как «it» → worries"),
 ("We plan ___ the new version next week. (launch)", ["to launch"], "Мы планируем выпустить новую версию на следующей неделе.", TO),
 ("I'm good at ___ complex things simple. (make)", ["making"], "Я умею делать сложное простым.", ING + ": good at making"),
 ("He ___ need me right now. (не нуждается)", ["doesn't", "does not"], "Сейчас я ему не нужна.", S),
]
ORD = [
 ("I want to ask you something.", "Я хочу кое-что у вас спросить.", TO),
 ("I'm continuing to work on the dashboard.", "Я продолжаю работать над дашбордом.", BE),
 ("The hardest part is meeting deadlines.", "Самое сложное — укладываться в сроки.", WHAT),
 ("I always meet my deadlines.", "Я всегда укладываюсь в сроки.", "meet a deadline — уложиться в срок; always перед глаголом"),
 ("What do you think?", "Как вы думаете?", "«Как вы думаете?» = What do you think? (не How you think?)"),
]
LESSON = {"id": R, "type": "lesson", "title": "Из вашей речи: to или -ing", "minutes": 4, "body": [
 "Ошибки из второго разговора 17.11. Хорошая новость: «X it's» почти ушло (5 → 2). Новая зона — что ставить после глагола: to или -ing.",
 "**Логика to:** to смотрит вперёд — на цель, на действие, которое ещё впереди. Поэтому после want, need, decide, plan, try, would like, hope → **to + глагол**: I want **to ask**. We decided **to make** it responsive.",
 "**Логика -ing:** -ing — действие как процесс или как «что-то». После enjoy, finish, keep, stop, mind → **-ing**: She enjoys **working**. Keep **going**.",
 "**После предлога — всегда -ing** (for, in, at, about, of, и to в look forward to): Thanks for **helping**. I'm good at **making** things simple. I'm interested in **learning**.",
 "**be + -ing — процесс сейчас:** I'm **working**, I'm **continuing** (не I'm work, I'm continue).",
 "**«Как не…»** → how **not to** forget: not стоит перед to.",
 "**Действие в роли «что»** → -ing: The hardest part is **meeting** deadlines.",
 "И снова -s: he/she/it + действие → it **scares** me, he **doesn't** answer. А things, users, they — без -s: the things that **worry** me."],
 "examples": [
  {"en": "I want to ask you something.", "ru": "Я хочу кое-что у вас спросить."},
  {"en": "I'm continuing to work on the dashboard.", "ru": "Я продолжаю работать над дашбордом."},
  {"en": "Thanks for helping me.", "ru": "Спасибо, что помогли мне."},
  {"en": "The hardest part is meeting deadlines.", "ru": "Самое сложное — укладываться в сроки."},
  {"en": "How not to forget new words?", "ru": "Как не забывать новые слова?"},
  {"en": "It scares me a little.", "ru": "Меня это немного пугает."}]}
def items(k):
    out = [{"kind": "fix", "q": q, "a": a, "explain": ru, "rule": R, "why": w} for q, a, ru, w in FIX[3*k:3*k+3]]
    out += [{"kind": "gap", "q": q, "a": a, "explain": ru, "rule": R, "why": w} for q, a, ru, w in GAP[2*k:2*k+2]]
    en, ru, w = ORD[k]; out.append({"kind": "order", "en": en, "ru": ru, "alt": [], "rule": R, "why": w})
    return out
src, dst, nid = sys.argv[1:4]
P = json.load(open(src))
for k, d in enumerate(P['days'][2:7]):
    g = d['general']; dn = k + 3
    pos = next((i + 1 for i, t in enumerate(g) if t['id'] == f'p3-d{dn}-s2'), len(g))
    block = [{"id": f"p3-d{dn}-s4", "type": "mix", "title": "Из вашей речи: to или -ing", "minutes": 3, "items": items(k)}]
    if k == 0: block.insert(0, LESSON)
    g[pos:pos] = block
P['replaces'] = sorted(set((P.get('replaces') or []) + [P['id']])); P['id'] = nid
json.dump(P, open(dst, 'w'), ensure_ascii=False, indent=1)
