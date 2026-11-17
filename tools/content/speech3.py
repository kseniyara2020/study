"""Блок «Из вашей речи: глагол + предлог, to или -ing» (разговор №3, 17.11): урок p3-d4-s5 (день 4), упражнение p3-dN-s6 (дни 4–7).
python3 tools/content/speech3.py packs/IN.json packs/OUT.json NEW_ID"""
import json, sys
R = 'p3-d4-s5'
TO = "decide / try / plan / hope + to + начальная форма глагола (после to — без -ed и без -s)"
HOW = "«как / что / где + сделать» → how / what / where + to + глагол"
NOUN = "существительное + to + глагол = «для чего»: an opportunity to go, a place to live (не for going)"
PREP_ING = "после предлога — -ing: dream of seeing, think about moving"
START = "start / begin — можно и -ing, и to: started doing = started to do"
PAIR = "глагол и его предлог — пара: wait for, look for, listen to, look at, think about, worry about, talk to … about, depend on"
END = "в вопросе предлог остаётся в конце, а вспомогательный глагол стоит перед подлежащим: What are you thinking about?"
QDO = "вопрос без be → нужен do / does / did перед подлежащим: What do you want?"
C3 = "о прошлом, которого не было: would have + 3-я форма (done, started, finished)"
FIX = [
 ("We decided to took a break.", ["We decided to take a break."], "Мы решили сделать перерыв.", TO),
 ("I tried do it myself.", ["I tried to do it myself."], "Я попыталась сделать это сама.", TO),
 ("I don't know how say it.", ["I don't know how to say it."], "Я не знаю, как это сказать.", HOW),
 ("I dreamed to see Paris.", ["I dreamed of seeing Paris.", "I dreamt of seeing Paris.", "I dreamed about seeing Paris.", "I dreamt about seeing Paris."], "Я мечтала увидеть Париж.", PREP_ING),
 ("It's a great opportunity for going abroad.", ["It's a great opportunity to go abroad.", "It is a great opportunity to go abroad."], "Это отличная возможность поехать за границу.", NOUN),
 ("What you are thinking about?", ["What are you thinking about?"], "О чём вы думаете?", END),
 ("Who are you waiting?", ["Who are you waiting for?"], "Кого вы ждёте?", PAIR + "; в вопросе for остаётся в конце"),
 ("What you want?", ["What do you want?"], "Что вы хотите?", QDO),
 ("I want to talk you about the deadline.", ["I want to talk to you about the deadline.", "I'd like to talk to you about the deadline."], "Я хочу поговорить с вами о сроке.", "talk to someone about something — с кем: to, о чём: about"),
 ("It depends of the client.", ["It depends on the client."], "Это зависит от клиента.", "depend on — «зависеть от» по-английски с on"),
 ("I wouldn't have start without your help.", ["I wouldn't have started without your help.", "I would not have started without your help."], "Без вашей помощи я бы не начала.", C3),
 ("We started do the research in May.", ["We started doing the research in May.", "We started to do the research in May.", "We started the research in May."], "Мы начали исследование в мае.", START),
]
GAP = [
 ("I'm looking ___ a new job. (ищу)", ["for"], "Я ищу новую работу.", PAIR),
 ("What are you listening ___? (слушаешь)", ["to"], "Что ты слушаешь?", END),
 ("I'm trying ___ a simpler solution. (find)", ["to find"], "Я пытаюсь найти решение попроще.", TO),
 ("Don't worry ___ the deadline. (насчёт)", ["about"], "Не переживай из-за срока.", PAIR),
 ("We need a quiet place ___. (work)", ["to work"], "Нам нужно тихое место, чтобы работать.", NOUN),
 ("The client put the project on ___ until January. (отложил)", ["hold"], "Клиент отложил проект до января.", "put something on hold — отложить, «заморозить» (B2)"),
 ("I wouldn't have ___ it without your help. (finish)", ["finished"], "Без вашей помощи я бы это не закончила.", C3),
 ("What ___ you looking at? (вопрос)", ["are"], "На что ты смотришь?", END),
]
ORD = [
 ("What are you thinking about?", "О чём вы думаете?", END),
 ("I don't know how to say it.", "Я не знаю, как это сказать.", HOW),
 ("I wouldn't have done it without you.", "Я бы не сделала этого без вас.", C3),
 ("We decided to put it on hold.", "Мы решили это отложить.", TO + "; put on hold — отложить"),
]
LESSON = {"id": R, "type": "lesson", "title": "Из вашей речи: глагол + предлог, to или -ing", "minutes": 4, "body": [
 "Ошибки из третьего разговора 17.11. Хорошая новость: -s стало лучше (he doesn't need, she doesn't give — верно), а «X it's» с паузой не появляется. Главная зона — что идёт после глагола.",
 "**to + начальная форма.** to смотрит вперёд, на действие, которое ещё впереди: decide **to take**, try **to do**, plan **to launch**. После to глагол всегда голый: не to took, не to does.",
 "**how / what / where + to.** Русское «как сказать», «что делать» → how **to** say, what **to** do. Без to фраза разваливается: how say — ошибка.",
 "**Существительное + to = «для чего».** an opportunity **to go**, a place **to live**, time **to rest**. Русское «для» тянет к for going — но for здесь не нужен.",
 "**После предлога — -ing.** dream **of seeing**, think **about moving**, thanks **for helping**. start и begin — можно и так, и так: started **doing** = started **to do**.",
 "**Глагол и предлог — пара, учим вместе:** wait **for**, look **for**, listen **to**, look **at**, think **about**, worry **about**, talk **to** someone **about** something, depend **on**.",
 "**В вопросе предлог остаётся в конце.** Логика: вопросительное слово уходит вперёд, а пара «глагол + предлог» не разрывается: What are you thinking **about**? Who are you waiting **for**? Если в вопросе нет be — нужен do: What **do** you want?",
 "**Готовый кусочек о прошлом, которого не было:** I **wouldn't have done** it without you — «без тебя я бы этого не сделала». would have + 3-я форма."],
 "examples": [
  {"en": "We decided to put it on hold.", "ru": "Мы решили это отложить."},
  {"en": "I don't know how to say it.", "ru": "Я не знаю, как это сказать."},
  {"en": "It's a great opportunity to go abroad.", "ru": "Это отличная возможность поехать за границу."},
  {"en": "What are you thinking about?", "ru": "О чём вы думаете?"},
  {"en": "Who are you waiting for?", "ru": "Кого вы ждёте?"},
  {"en": "I wouldn't have done it without you.", "ru": "Я бы не сделала этого без вас."}]}
def items(k):
    out = [{"kind": "fix", "q": q, "a": a, "explain": ru, "rule": R, "why": w} for q, a, ru, w in FIX[3*k:3*k+3]]
    out += [{"kind": "gap", "q": q, "a": a, "explain": ru, "rule": R, "why": w} for q, a, ru, w in GAP[2*k:2*k+2]]
    en, ru, w = ORD[k]; out.append({"kind": "order", "en": en, "ru": ru, "alt": [], "rule": R, "why": w})
    return out
src, dst, nid = sys.argv[1:4]
P = json.load(open(src))
for k, d in enumerate(P['days'][3:7]):
    g = d['general']; dn = k + 4
    pos = max((i + 1 for i, t in enumerate(g) if t['id'].split('-')[-1].startswith('s')), default=len(g))
    block = [{"id": f"p3-d{dn}-s6", "type": "mix", "title": "Из вашей речи: глагол + предлог, to или -ing", "minutes": 3, "items": items(k)}]
    if k == 0: block.insert(0, LESSON)
    g[pos:pos] = block
P['replaces'] = sorted(set((P.get('replaces') or []) + [P['id']])); P['id'] = nid
json.dump(P, open(dst, 'w'), ensure_ascii=False, indent=1)
