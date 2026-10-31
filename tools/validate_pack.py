#!/usr/bin/env python3
"""Проверка пакета перед публикацией: python3 tools/validate_pack.py packs/pack-003.json
Проверяет схему, уникальность id по всем пакетам в packs/, индексы ответов, ссылки на слова, время дня."""
import json, sys, glob, os
KINDS = {'choice', 'gap', 'dictation', 'translate', 'fix', 'order', 'shadow'}
TYPES = {'lesson', 'cards', 'quiz', 'dialog', 'gap', 'dictation', 'write', 'mix', 'translate', 'fix', 'order', 'shadow'}
def fail(m): print('ОШИБКА:', m); sys.exit(1)
path = sys.argv[1]; p = json.load(open(path))
if p.get('type') != 'study-pack': fail('type должен быть study-pack')
for k in ('id', 'title', 'level', 'created', 'days'):
    if k not in p: fail('нет поля ' + k)
here = os.path.dirname(os.path.abspath(path))
other_ids, other_vocab = set(), {}
for f in glob.glob(os.path.join(here, 'pack-*.json')):
    if os.path.abspath(f) == os.path.abspath(path): continue
    o = json.load(open(f))
    for d in o.get('days', []):
        for s in ('general', 'ux'):
            for t in d.get(s, []): other_ids.add(t['id'])
    for m in o.get('media', []):
        for t in m.get('tasks', []): other_ids.add(t['id'])
    for v in o.get('vocab', []): other_vocab[v['id']] = v
V = {v['id']: v for v in p.get('vocab', [])}
for vid, v in V.items():
    if vid in other_vocab and other_vocab[vid]['en'] != v['en']: fail(f'id слова {vid} уже занят другим словом')
ids = []
def check_task(t, where):
    if t.get('type') not in TYPES: fail(f'{where}: неизвестный type {t.get("type")}')
    if not t.get('id') or not t.get('title'): fail(f'{where}: нет id/title')
    ids.append(t['id'])
    if not isinstance(t.get('minutes'), (int, float)): fail(f'{t["id"]}: нет minutes')
    for c in t.get('cards', []):
        if c not in V and c not in other_vocab: fail(f'{t["id"]}: слово {c} не найдено в vocab')
    for i, it in enumerate(t.get('items', [])):
        k = it.get('kind') or ('choice' if t['type'] in ('quiz', 'dialog') else t['type'])
        w = f'{t["id"]}[{i}]'
        if k not in KINDS: fail(f'{w}: неизвестный kind {k}')
        if k == 'choice':
            if not (0 <= it['a'] < len(it['options'])): fail(f'{w}: индекс ответа вне вариантов')
            if len(set(it['options'])) != len(it['options']): fail(f'{w}: повторяются варианты')
        elif k == 'order':
            if len(it['en'].split()) < 3: fail(f'{w}: слишком короткая фраза для сборки')
        elif k == 'shadow':
            if not it.get('en'): fail(f'{w}: нет en')
        else:
            if not isinstance(it.get('a'), list) or not it['a']: fail(f'{w}: a должен быть непустым списком')
            if k == 'translate' and not it.get('ru'): fail(f'{w}: нет ru')
            if k == 'fix' and it['q'] in it['a']: fail(f'{w}: в fix неверное предложение совпадает с ответом')
            if k == 'gap' and '___' not in it.get('q', ''): fail(f'{w}: в gap нет ___')
    if t['type'] == 'dialog' and not t.get('lines'): fail(f'{t["id"]}: dialog без lines')
    if t['type'] == 'write' and not t.get('prompt'): fail(f'{t["id"]}: write без prompt')
for d in p['days']:
    for s in ('general', 'ux'):
        for t in d.get(s, []): check_task(t, f'день {d["day"]}/{s}')
    m = sum(t['minutes'] for s in ('general', 'ux') for t in d.get(s, []))
    n = sum(len(t.get('items', [])) for s in ('general', 'ux') for t in d.get(s, []))
    print(f'День {d["day"]}: {d.get("title","")} — {m} мин, {n} заданий')
    if m < 20: fail(f'день {d["day"]}: меньше 20 минут')
for mi in p.get('media', []):
    for k in ('id', 'kind', 'title', 'url', 'source', 'level', 'tasks'):
        if k not in mi: fail(f'media {mi.get("id")}: нет {k}')
    if mi['kind'] not in ('article', 'podcast', 'series'): fail(f'media {mi["id"]}: kind article|podcast')
    for t in mi['tasks']: check_task(t, 'media ' + mi['id'])
if len(ids) != len(set(ids)): fail('повторяются id заданий внутри пакета')
dup = set(ids) & other_ids
if dup: fail('id уже есть в других пакетах: ' + ', '.join(sorted(dup)[:5]))
print('OK:', p['id'], '—', len(ids), 'заданий-блоков')
