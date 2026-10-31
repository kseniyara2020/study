import json, os, shutil
from PIL import Image, ImageDraw, ImageFont
ROOT='/home/claude'; D=ROOT+'/dist'
shutil.rmtree(D, ignore_errors=True); os.makedirs(D+'/packs'); os.makedirs(D+'/icons')
pack=json.load(open(ROOT+'/pack-002.json'))
test=json.load(open(ROOT+'/level-v1.json'))
import datetime
BUILD=(datetime.datetime.utcnow()+datetime.timedelta(hours=3)).strftime('%d.%m %H:%M')
src=open(ROOT+'/app.src.html').read().replace('__SEED_TEST__', json.dumps(test,ensure_ascii=False).replace('</','<\\/')).replace('__BUILD__', BUILD).replace('__SEED__', json.dumps(pack,ensure_ascii=False).replace('</','<\\/'))
open(ROOT+'/study-app.html','w').write(src)  # artifact preview
title_end=src.index('</title>')+8
head_extra='''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F2F2F7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-title" content="Учёба">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" href="icons/icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
'''
body=src[title_end:]
# split head-ish tags (meta + style) from body content
style_end=body.index('</style>')+8
html=head_extra+src[:title_end]+body[:style_end]+'\n</head>\n<body>\n'+body[style_end:]+'\n</body>\n</html>\n'
open(D+'/index.html','w').write(html)
json.dump({"name":"Мой учебный план","short_name":"Учёба","lang":"ru","start_url":"./","scope":"./","display":"standalone",
 "background_color":"#F2F2F7","theme_color":"#5856D6",
 "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png"},
          {"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
 open(D+'/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
open(D+'/sw.js','w').write('''const CACHE='study-v6';
const SHELL=['./','index.html','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png','icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url); if(e.request.method!=='GET'||u.origin!==location.origin)return;
  // app shell + packs: network first, cache as offline fallback
  e.respondWith(fetch(e.request,{cache:'no-cache'}).then(r=>{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r;}).catch(()=>caches.match(e.request).then(m=>m||caches.match('index.html'))));
});
''')
shutil.copy(ROOT+'/pack-001.json', D+'/packs/pack-001.json')
shutil.copy(ROOT+'/pack-002.json', D+'/packs/pack-002.json')
shutil.copy(ROOT+'/level-v1.json', D+'/packs/level-v1.json')
json.dump({"packs":[{"id":pack['id'],"file":"pack-002.json","title":pack['title'],"created":pack['created']}],"levelTests":[{"id":test['id'],"file":"level-v1.json","version":test['version']}],"results":[]},open(D+'/packs/index.json','w'),ensure_ascii=False,indent=1)
# icon: indigo rounded tile with stacked cards + "En"
def icon(size, path, rounded=False):
    s=size*4; im=Image.new('RGBA',(s,s),(0,0,0,0)); d=ImageDraw.Draw(im)
    top=(110,108,232); bot=(76,70,196)
    for y in range(s):
        t=y/s; d.line([(0,y),(s,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))+(255,))
    w=s*0.46; h=s*0.56; cx=s/2; cy=s/2+s*0.02
    d.rounded_rectangle([cx-w/2+s*0.06,cy-h/2-s*0.06,cx+w/2+s*0.06,cy+h/2-s*0.06],radius=s*0.06,fill=(255,255,255,90))
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=s*0.06,fill=(255,255,255,255))
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(s*0.2))
    except Exception: f=ImageFont.load_default()
    d.text((cx,cy-s*0.03),"En",font=f,fill=(88,86,214,255),anchor='mm')
    d.rounded_rectangle([cx-w*0.3,cy+h*0.24,cx+w*0.3,cy+h*0.24+s*0.025],radius=s*0.0125,fill=(88,86,214,110))
    im=im.resize((size,size),Image.LANCZOS)
    if not rounded: im=im.convert('RGB')
    im.save(path)
icon(512,D+'/icons/icon-512.png'); icon(192,D+'/icons/icon-192.png'); icon(180,D+'/icons/apple-touch-icon.png')
print(sorted(os.path.relpath(os.path.join(r,f),D) for r,_,fs in os.walk(D) for f in fs))
