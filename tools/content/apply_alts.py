# Usage: python3 tools/content/apply_alts.py packs/IN.json packs/OUT.json NEW_ID
# Copies a pack, adds all correct alternatives from banks.py (alt lists + UX_ALT) to `a` / `alt`
# of every item, and makes the copy replace the input pack (task ids stay the same → progress is kept).
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banks
src, dst, new_id = sys.argv[1:4]
p = json.load(open(src))
ALT = {}
for k, v in banks.UX_ALT.items(): ALT.setdefault(k, []); ALT[k] += [x for x in v if x not in ALT[k]]
for name in dir(banks):
    r = getattr(banks, name)
    if isinstance(r, tuple) and len(r) == 3 and isinstance(r[2], list):
        for row in r[2]:
            if len(row) >= 7 and row[6]:
                ALT.setdefault(row[0], []); ALT[row[0]] += [x for x in row[6] if x not in ALT[row[0]]]
GAP = {"Can you ___ the problem with the icons?": ["figure out"]}   # gap words that are also correct
n = 0
for d in p['days']:
    for sec in ('general', 'ux'):
        for t in d.get(sec, []):
            for it in t.get('items', []):
                a = it.get('a')
                if isinstance(a, list) and a:
                    extra = [x for x in ALT.get(a[0], []) if x not in a]
                    for q, ws in GAP.items():
                        if it.get('kind') == 'gap' and it.get('q', '').startswith(q): extra += [w for w in ws if w not in a]
                    if extra: it['a'] = a + extra; n += len(extra)
                if it.get('kind') == 'order' and it.get('en') in ALT:
                    extra = [x for x in ALT[it['en']] if x not in it.get('alt', [])]
                    if extra: it['alt'] = it.get('alt', []) + extra; n += len(extra)
old = p['id']; p['id'] = new_id
p['replaces'] = sorted(set((p.get('replaces') or []) + [old]))
json.dump(p, open(dst, 'w'), ensure_ascii=False, indent=1)
print(new_id, 'replaces', p['replaces'], '+alts', n)
