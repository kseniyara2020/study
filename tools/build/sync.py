"""Синхронизация исходника приложения: tools/app.js → index.html и tools/app.src.html.
Запуск из корня репозитория: python3 tools/build/sync.py
Подставляет __BUILD__ (дата/время сборки, Минск) в index.html; CSS-правки ниже идемпотентны.
Только после подтверждения пользователя на изменение кода (см. claude/export-import-rules.md §7)."""
import sys, os, datetime, re
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app=open(ROOT+'/tools/app.js').read()
CSS_OLD=""".diff{display:flex;flex-direction:column;gap:6px;margin-top:6px;font-size:var(--fs-body);line-height:24px}
.dlbl{display:inline-block;min-width:92px;font-size:var(--fs-foot);color:var(--label2)}
.dw-bad{color:var(--red);text-decoration-thickness:1.5px}
.dw-good{color:var(--green);font-weight:700;background:var(--green-soft);border-radius:4px;padding:0 3px}"""
CSS_NEW=""".diff{display:flex;flex-direction:column;margin-top:4px}
.dlbl{display:block;margin-top:10px;font-size:var(--fs-foot);color:var(--label2)}
.dline{font-size:var(--fs-body);line-height:24px}
.dw-bad{color:var(--red);font-weight:600}
.dw-good{color:var(--green);font-weight:700}
.fb-why{margin-top:2px}.fb-why .dlbl{margin-bottom:2px}
.fb-tr{margin-top:10px;font-size:var(--fs-sub);color:var(--label2)}
.fb .rule-btn{margin-top:14px;width:100%}
.link-btn{background:none;border:0;padding:0;margin-top:10px;color:var(--accent);font:inherit;font-size:var(--fs-sub);cursor:pointer}
.qfoot{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.qfoot .link-btn{margin-top:8px;font-size:13px}
.seg-chips{display:flex;gap:8px;overflow-x:auto;margin:0 0 12px;padding-bottom:2px}"""
TAG=".topic-tag{display:inline-block;margin:0 0 8px;padding:3px 10px;border-radius:12px;background:var(--fill);color:var(--label2);font-size:13px;line-height:18px}\n"
build=(datetime.datetime.utcnow()+datetime.timedelta(hours=3)).strftime('%d.%m %H:%M')
for f,b in [(ROOT+'/index.html',build),(ROOT+'/tools/app.src.html',None)]:
    s=open(f).read()
    i=s.index('<script>\n(function(){\n')+len('<script>\n'); j=s.rindex('})();')+len('})();\n')
    body=app if b is None else app.replace('__BUILD__',b)
    s=s[:i]+body+s[j:]
    if CSS_OLD in s: s=s.replace(CSS_OLD,CSS_NEW)
    if '.topic-tag{' not in s: s=s.replace('.seg-chips{', TAG+'.seg-chips{',1)
    elif '.dline{' not in s: print('CSS not found',f); sys.exit(1)
    open(f,'w').write(s); print('synced',f)
