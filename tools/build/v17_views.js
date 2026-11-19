/* ---------- v17 design helpers (19.11.2026) ---------- */
function ctaHtml(act, attrs, title, trail, sub, icon) {
  return `<button class="cta" data-act="${act}" ${attrs || ''}><span class="ci">${icon || IC.play}</span><span class="ct"><b>${esc(title)}${trail ? ` <em>${esc(trail)}</em>` : ''}</b>${sub ? `<span>${esc(sub)}</span>` : ''}</span></button>`;
}
function pbarHtml(pct) { return `<span class="pbar"><i style="width:${Math.max(0, Math.min(100, pct))}%"></i></span>`; }
function weekHtml() {
  const t = today(), d0 = parse(t), wd = (d0.getDay() + 6) % 7, mon = addDays(t, -wd);
  const names = lang() === 'en' ? ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] : ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
  let cells = '';
  for (let i = 0; i < 7; i++) { const d = addDays(mon, i), on = !!S.activity[d]; cells += `<div class="${d === t ? 't' : ''} ${d < t ? 'past' : ''} ${on ? 'on' : ''}"><span>${names[i]}</span><b>${parse(d).getDate()}</b><i></i></div>`; }
  const sun = addDays(mon, 6);
  return `<div class="wk-cap">${L('Неделя', 'Week')} · ${fmtDate(mon, { day: 'numeric', month: 'short' })} – ${fmtDate(sun, { day: 'numeric', month: 'short' })}</div><div class="wk">${cells}</div>`;
}
function shortDur(days) { return days >= 60 ? Math.round(days / 30) + L('мес', 'm') : days >= 14 ? Math.round(days / 7) + L('н', 'w') : days + L('д', 'd'); }
function daysSince(d) { return Math.max(0, Math.round((parse(today()) - parse(d)) / 864e5)); }
function lastTalk() { const l = (S.speaking || []).map(r => r.date).sort(); return l[l.length - 1] || null; }
function sTile(sec, val, unit, name, sub, pct, act, attrs) {
  return `<button class="stile sec-${sec}" data-act="${act}" ${attrs || ''}><span class="v">${esc(String(val))}${unit ? `<small>${esc(unit)}</small>` : ''}</span><span><span class="n">${esc(name)}</span><span class="s">${esc(sub)}</span>${pct == null ? '' : pbarHtml(pct)}</span></button>`;
}
function dayTiles(p, di) {
  const d = p && p.days[di];
  const g = d ? secStats(d.general || []) : { done: 0, total: 0, plan: 0, spent: 0 }, u = d ? secStats(d.ux || []) : { done: 0, total: 0, plan: 0, spent: 0 };
  const left = st => Math.max(0, st.plan - st.spent);
  const due = dueCards().length, total = Object.keys(S.cards).length, lt = lastTalk();
  let h = '<div class="tiles4">';
  h += sTile('general', g.done, '/' + g.total, L('Общий', 'General'), g.total ? (g.done === g.total ? L('готово', 'done') : '~' + left(g) + ' ' + L('мин осталось', 'min left')) : L('нет заданий', 'no tasks'), g.total ? Math.round(g.done / g.total * 100) : 0, 'open-daysec', `data-sec="general" data-di="${di}"`);
  h += sTile('ux', u.done, '/' + u.total, 'UX/UI', u.total ? (u.done === u.total ? L('готово', 'done') : '~' + left(u) + ' ' + L('мин осталось', 'min left')) : L('нет заданий', 'no tasks'), u.total ? Math.round(u.done / u.total * 100) : 0, 'open-daysec', `data-sec="ux" data-di="${di}"`);
  h += sTile('words', due, '', L('Слова', 'Words'), total ? (due ? L('на повторение', 'to review today') : L('всё повторено', 'all reviewed')) : L('пока нет слов', 'no words yet'), null, 'open-review');
  h += sTile('speaking', lt ? shortDur(daysSince(lt)) : '—', '', L('Говорение', 'Speaking'), lt ? L('с последнего разговора', 'since last talk') : L('по желанию', 'optional'), null, 'open-speaking');
  return h + '</div>';
}
function coverHtml(kind, label, sm) {
  if (kind === 'series') return `<span class="cov series ${sm ? 'sm' : ''}" aria-hidden="true">${esc(label || '')}</span>`;
  if (kind === 'article') return `<span class="cov article ${sm ? 'sm' : ''}" aria-hidden="true"><b>${esc(label || '')}</b><i></i><i></i><i></i></span>`;
  return `<span class="cov podcast ${sm ? 'sm' : ''}" aria-hidden="true">${[12, 26, 16, 34, 20, 28, 10].map(x => `<i style="height:${sm ? x : Math.round(x * 1.3)}px"></i>`).join('')}</span>`;
}
const srcShort = s => { s = String(s || ''); const m = s.match(/\b(NN\/g|BBC|TED)\b/i); if (m) return m[1]; const w = s.replace(/^The\s+/i, '').split(/\s+/).filter(Boolean); return w.length > 1 ? w.map(x => x[0]).join('').slice(0, 3).toUpperCase() : s.slice(0, 5); };
function mediaCounts(m) { const ts = m.tasks || [], d = ts.filter(t => isDone(t.id)).length; return { d, n: ts.length, full: ts.length > 0 && d === ts.length }; }
function mediaCard(m) {
  const c = mediaCounts(m), kind = m.kind === 'podcast' ? 'podcast' : 'article';
  const eyebrow = [m.kind === 'podcast' ? L('Подкаст', 'Podcast') : L('Статья', 'Article'), m.topic === 'ux' ? 'UX' : L('общая тема', 'general'), m.source].filter(Boolean).join(' · ');
  const st = c.full ? L('Все задания выполнены', 'All tasks done') + ` · ${c.n}` : c.d ? `${c.d} ${L('из', 'of')} ${c.n} ${L('заданий', 'tasks')}` : `${L('Новое', 'New')} · ${c.n} ${L('заданий', 'tasks')}`;
  return `<button class="mc ${c.full ? 'done' : 'glow'} sec-media" data-act="open-media" data-id="${esc(m.id)}"><span class="mr">${coverHtml(kind, srcShort(m.source))}<span class="mi"><span class="me"><span>${esc(eyebrow)}</span>${c.full ? IC.check : ''}</span>
    <span class="mt">${esc(m.title)}</span><span class="mm">${esc([m.level, mins(m.minutes)].filter(Boolean).join(' · '))}</span><span class="ms">${esc(st)}</span></span></span>${c.n ? pbarHtml(c.d / c.n * 100) : ''}</button>`;
}
function mediaRow(kind, label, title, typ, meta, act, attrs, first) {
  return `<button class="row" data-act="${act}" ${attrs}>${coverHtml(kind, label, true)}<span class="row-main"><span class="mrt">${esc(title)}</span><span class="mrk">${esc(typ)}</span><span class="mrm">${esc(meta)}</span></span>${IC.chevR}</button>`;
}
function nextCheckText() {
  const w = checkWindow(); if (!w) return '—';
  const t = today();
  if (t < w.from) { const n = Math.round((parse(w.from) - parse(t)) / 864e5); return L('через ', 'in ') + (n >= 14 ? Math.round(n / 7) + ' ' + P(Math.round(n / 7), 'неделю', 'недели', 'недель', 'week', 'weeks') : n + ' ' + P(n, 'день', 'дня', 'дней', 'day', 'days')); }
  if (t <= w.to) return L('сейчас', 'now');
  return L('ждёт', 'waiting');
}

/* ---------- Today ---------- */
function vToday() {
  const p = activePack();
  if (!p) return { title: L('Сегодня', 'Today'), body: empty(IC.box, L('Нет пакета заданий', 'No task pack'), L('Попросите Claude собрать пакет и импортируйте его в Настройках.', 'Ask Claude for a pack and import it in Settings.')) };
  const di = currentDayIndex(p), d = p.days[di];
  const all = dayTasks(d), done = all.filter(t => isDone(t.id)).length, pct = all.length ? Math.round(done / all.length * 100) : 0;
  const next = all.find(t => !isDone(t.id));
  const secOf = t => (d.ux || []).includes(t) ? 'ux' : 'general';
  const topicSec = next ? secOf(next) : 'general';
  const parts = ['general', 'ux'].filter(s => req(d[s] || []).length).map(s => SECTIONS[s].short()).join(' + ');
  let h = checkBanner();
  h += `<div class="dcard sec-${topicSec}">${weekHtml()}
    <div class="dsep"><div class="wk-cap">${L('Тема дня', 'Today’s topic')} · ${esc(SECTIONS[topicSec].name())}</div><div class="dtop">${esc(d.title)}</div>
    <div class="dprog"><span><b>${done} ${L('из', 'of')} ${all.length}</b> · ${esc(parts)}</span><em>${pct}%</em></div>${pbarHtml(pct)}</div>
    ${next ? ctaHtml('open-task', `data-id="${esc(next.id)}"`, L('Продолжить', 'Continue'), '· ' + mins(next.minutes), L('Дальше: ', 'Next: ') + next.title) : `<div class="dprog" style="justify-content:center"><b>${L('Всё готово на сегодня', 'All done for today')}</b></div>`}</div>`;
  h += groupHead(L('Английский', 'English'), `<button class="glink" data-act="tab" data-tab="english">${L('Все', 'All')}</button>`) + dayTiles(p, di);
  if (S.settings.mediaNudge) {
    const rows = [];
    S.shows.forEach(sh => { const n = S.myWords.filter(w => w.show === sh.id).length; rows.push(mediaRow('series', sh.current || '', sh.title + ' · ' + (sh.current || ''), L('Сериал', 'Series'), n + ' ' + P(n, 'слово записано', 'слова записано', 'слов записано', 'word saved', 'words saved'), 'open-show', `data-id="${esc(sh.id)}"`)); });
    (S.media || []).filter(m => !mediaCounts(m).full).slice(0, 2).forEach(m => { const c = mediaCounts(m); rows.push(mediaRow(m.kind === 'podcast' ? 'podcast' : 'article', srcShort(m.source), m.title, m.kind === 'podcast' ? L('Подкаст', 'Podcast') : L('Статья', 'Article'), [m.level, mins(m.minutes), c.n ? `${c.d}/${c.n}` : ''].filter(Boolean).join(' · '), 'open-media', `data-id="${esc(m.id)}"`)); });
    if (rows.length) h += groupHead(L('Медиа', 'Media'), `<button class="glink" data-act="tab" data-tab="media">${L('Все', 'All')}</button>`) + `<div class="group mlist">${rows.join('')}</div>`;
  }
  const sp = latestLevel('speaking'), li = latestLevel('listening');
  h += groupHead(L('Прогресс', 'Progress'), `<button class="glink" data-act="tab" data-tab="progress">${L('Подробнее', 'Details')}</button>`) +
    `<div class="pcard glow wide sec-general"><div class="pstats"><div><b>${shortDur(streak())}</b><span>${L('серия', 'Streak')}</span></div><div><b>${sp ? esc(sp.level) : '—'}</b><span>${L('Говорение', 'Speaking')}</span></div><div><b>${li ? esc(li.level) : '—'}</b><span>${L('Аудирование', 'Listening')}</span></div></div>
    <div class="pfoot"><span>${L('Следующая проверка', 'Next level check')}</span><b>${esc(nextCheckText())}</b></div></div>`;
  return { title: L('Сегодня', 'Today'), pill: `${L('День', 'Day')} ${d.day} ${L('из', 'of')} ${p.days.length}`, body: h };
}

/* ---------- English ---------- */
function vEnglish() {
  const p = activePack();
  if (!p) return { title: L('Английский', 'English'), body: empty(IC.box, L('Нет пакета заданий', 'No task pack'), '') };
  const ci = currentDayIndex(p);
  let h = groupHead(L('Ежедневно', 'Daily')) + dayTiles(p, ci);
  h += groupHead(L('Эта неделя', 'This week'));
  h += '<div class="group">' + p.days.map((d, i) => {
    const list = dayTasks(d), all = list.length && list.every(t => isDone(t.id)), now = i === ci && !all;
    return `<button class="row" data-act="open-daysec" data-sec="general" data-di="${i}"><span class="check ${all ? 'on' : now ? 'now' : ''}">${all ? IC.check : ''}</span>
      <span class="row-main"><span class="row-title" ${all ? 'style="color:var(--label2)"' : ''}>${esc(d.title)}</span><span class="row-sub">${L('День', 'Day')} ${d.day} · ${list.filter(t => isDone(t.id)).length}/${list.length}</span></span>${now ? `<span class="nowtag">${L('Сейчас', 'Now')}</span>` : ''}${IC.chevR}</button>`;
  }).join('') + '</div>';
  h += '<div class="group" style="margin-top:8px">' + ['general', 'ux'].map(sec => `<button class="row" data-act="open-section" data-sec="${sec}"><span class="row-main"><span class="row-title">${L('Все задания', 'All tasks')} · ${esc(SECTIONS[sec].short())}</span><span class="row-sub">${L('все дни всех пакетов', 'all days of all packs')}</span></span>${IC.chevR}</button>`).join('') + '</div>';
  const st = reviewStats();
  if (st.pending || st.reviewed || st.texts) {
    const acc = st.reviewed ? Math.round((st.ok + st.almost * 0.5) / st.reviewed * 100) : 0;
    h += groupHead(L('Проверка Claude', 'Claude’s review'), `<button class="glink" data-act="open-reviews">${L('Все', 'All')}</button>`) +
      `<button class="pcard glow wide sec-general" data-act="open-reviews" style="width:100%;text-align:inherit;font:inherit;cursor:pointer"><div class="pstats"><div><b>${st.reviewed ? acc + '%' : '—'}</b><span>${L('переводы', 'translations')}</span></div><div><b>${st.pending}</b><span>${L('ждут проверки', 'being checked')}</span></div><div><b>${st.textsDone}</b><span>${L('текстов', 'texts')}</span></div></div>
      <div class="pfoot"><span>${st.pending ? L('Сделайте экспорт для Claude', 'Make an export for Claude') : L('Всё проверено', 'All checked')}</span></div></button>`;
  }
  return { title: L('Английский', 'English'), pill: `${L('День', 'Day')} ${p.days[ci].day} ${L('из', 'of')} ${p.days.length}`, body: h };
}

/* ---------- Section of a day ---------- */
function vDaySec(sec, di) {
  const p = activePack(), d = p && p.days[di];
  if (!d) return { title: SECTIONS[sec].name(), back: true, sec, body: '' };
  const list = d[sec] || [], st = secStats(list), next = req(list).find(t => !isDone(t.id)), opt = list.filter(isOptional);
  const pct = st.total ? Math.round(st.done / st.total * 100) : 0;
  let sc = 0, tot = 0; req(list).forEach(t => { const pr = S.progress[t.id]; if (pr && pr.done && pr.total) { sc += pr.score; tot += pr.total; } });
  let h = `<div class="hero glow"><div class="big2"><b>${st.done}<small>/${st.total}</small></b><em>${pct}%</em></div>${pbarHtml(pct)}
    <div class="meta"><span>${st.spent} ${L('из', 'of')} ~${st.plan} ${L('мин', 'min')}</span><span>${tot ? Math.round(sc / tot * 100) + '% ' + L('верно', 'correct') : ''}</span></div>
    ${next ? ctaHtml('open-task', `data-id="${esc(next.id)}"`, L('Продолжить', 'Continue'), '· ' + mins(next.minutes), L('Дальше: ', 'Next: ') + next.title) : ''}</div>`;
  h += groupHead(L('Задания', 'Tasks')) + `<div class="group">${req(list).map(t => taskRow(t, next && t.id === next.id)).join('')}</div>`;
  if (opt.length) h += groupHead(L('Дополнительно · по желанию', 'Extra · optional')) + `<div class="group">${opt.map(t => taskRow(t)).join('')}</div><div class="gfoot">${L('Послушайте и повторите фразы дня. Не входит в план дня.', 'Listen and repeat the day’s phrases. Not part of the daily plan.')}</div>`;
  return { title: sec === 'ux' ? 'UX/UI' : SECTIONS[sec].short(), back: true, sec, pill: `${L('День', 'Day')} ${d.day} ${L('из', 'of')} ${p.days.length}`, sub: esc(d.title), body: h };
}

/* ---------- Media ---------- */
function vMedia() {
  const seg = UI.mseg || 'series';
  let h = `<div class="seg" role="tablist"><button class="${seg === 'series' ? 'on' : ''}" data-act="media-seg" data-seg="series">${L('Сериалы', 'Series')}</button><button class="${seg === 'article' ? 'on' : ''}" data-act="media-seg" data-seg="article">${L('Статьи', 'Articles')}</button><button class="${seg === 'podcast' ? 'on' : ''}" data-act="media-seg" data-seg="podcast">${L('Подкасты', 'Podcasts')}</button></div>`;
  if (seg === 'series') {
    h += groupHead(L('Смотрю', 'Watching'));
    S.shows.forEach(sh => {
      const n = S.myWords.filter(w => w.show === sh.id).length, w = (sh.watched || []).length;
      h += `<button class="mc glow sec-media" data-act="open-show" data-id="${esc(sh.id)}"><span class="mr">${coverHtml('series', sh.title)}<span class="mi"><span class="me"><span>${L('Сериал', 'Series')}</span></span>
        <span class="mt">${esc(sh.title)}</span><span class="mm">${L('Сейчас', 'Now')}: ${esc(sh.current || '')} · ${n} ${P(n, 'слово', 'слова', 'слов', 'word', 'words')}</span><span class="ms">${w} ${P(w, 'серия просмотрена', 'серии просмотрены', 'серий просмотрено', 'episode watched', 'episodes watched')}</span></span></span></button>`;
    });
    h += `<div class="gfoot">${L('Новые сериалы приходят с пакетами от Claude — напишите в чат.', 'New series come with packs from Claude — ask in the chat.')}</div>`;
  } else {
    const list = (S.media || []).filter(m => m.kind === seg);
    if (!list.length) h += empty(seg === 'article' ? IC.read : IC.ear, seg === 'article' ? L('Пока нет статей', 'No articles yet') : L('Пока нет подкастов', 'No podcasts yet'), L('Claude добавит их вместе со следующим пакетом.', 'Claude will add them with the next pack.'));
    else {
      const open = list.filter(m => !mediaCounts(m).full).map((m, i) => ({ m, i })).sort((a, b) => ((mediaCounts(b.m).d > 0) - (mediaCounts(a.m).d > 0)) || a.i - b.i).map(x => x.m), done = list.filter(m => mediaCounts(m).full);
      if (open.length) h += groupHead((seg === 'article' ? L('Читать', 'To read') : L('Слушать', 'To listen')) + ' · ' + open.length) + open.map(mediaCard).join('');
      if (done.length) h += groupHead(L('Пройдено', 'Done') + ' · ' + done.length) + done.map(mediaCard).join('');
    }
  }
  return { title: L('Медиа', 'Media'), pill: L('По желанию', 'Optional'), sec: 'media', body: h };
}
function vShow(id) {
  const sh = S.shows.find(s => s.id === id);
  if (!sh) return { title: L('Медиа', 'Media'), back: true, sec: 'media', body: empty(IC.tv, L('Сериал не найден', 'Series not found'), '') };
  const all = S.myWords.filter(w => w.show === id);
  let h = `<div class="hero glow"><div class="mr" style="display:flex;gap:16px">${coverHtml('series', sh.title)}<span class="mi" style="display:flex;flex-direction:column;min-width:0"><span style="font-size:13px;color:var(--label2)">${L('Сейчас смотрю', 'Now watching')}</span>
    <span style="margin-top:2px;font-size:22px;line-height:27px;font-weight:700">${esc(sh.current || '')}</span><span style="margin-top:4px;font-size:13px;line-height:17px;color:var(--label2)">${L('Записывайте незнакомые слова во время просмотра — Claude соберёт по ним задания.', 'Save unknown words while you watch — Claude builds tasks from them.')}</span>
    <span style="margin-top:auto;padding-top:8px;font-size:13px;font-weight:600;color:var(--sec)">${all.length} ${P(all.length, 'слово записано', 'слова записано', 'слов записано', 'word saved', 'words saved')}</span></span></div>
    ${ctaHtml('add-word', '', L('Записать слово', 'Save a word'), '', '', IC.plus)}</div>`;
  h += groupHead(L('Мои слова', 'My words') + ' · ' + all.length);
  if (!all.length) h += `<div class="empty">${IC.plus}<b>${L('Пока нет слов', 'No words yet')}</b>${L('Во время просмотра нажмите «Записать слово».', 'While watching, tap “Save a word”.')}</div>`;
  else {
    const eps = [...new Set(all.map(w => w.ep))].sort().reverse();
    eps.forEach((ep, k) => {
      const ws = all.filter(w => w.ep === ep);
      h += `<div class="lbl" style="margin:${k ? 16 : 0}px 4px 8px">${esc(ep)} · ${ws.length}</div><div class="group">` + ws.map(w => `<div class="row static">
        <button class="play small" data-act="speak" data-text="${esc(w.text)}" aria-label="${L('Произнести', 'Play')}">${IC.play}</button>
        <span class="row-main"><span class="row-title">${esc(w.text)}</span><span class="row-sub">${w.ru ? esc(w.ru) : L('Перевод — в задании от Claude', 'Translation will come in a task from Claude')}${w.ctx ? ' · ' + esc(w.ctx) : ''}</span></span>
        <button class="del" data-act="del-word" data-id="${esc(w.id)}" aria-label="${L('Удалить', 'Delete')}">${IC.trash}</button></div>`).join('') + '</div>';
    });
  }
  const eps = sh.episodes || [{ ep: sh.current }];
  h += groupHead(L('Сезон 1', 'Season 1')) + '<div class="group">' + eps.map(e => {
    const w = (sh.watched || []).includes(e.ep), n = all.filter(x => x.ep === e.ep).length;
    return `<div class="row static"><span class="check ${w ? 'on' : ''}">${w ? IC.check : ''}</span>
      <span class="row-main"><span class="row-title">${esc(e.ep)} ${esc(e.title || '')}</span>
      <span class="row-sub">${w ? L('Просмотрено', 'Watched') : L('Не просмотрено', 'Not watched')} · ${n} ${P(n, 'слово', 'слова', 'слов', 'word', 'words')}</span></span>
      ${w ? '' : `<button class="chip on" data-act="watched" data-ep="${esc(e.ep)}">${L('Посмотрела', 'Watched')}</button>`}</div>`;
  }).join('') + `</div><div class="gfoot">${L('Задания по серии приходят с пакетом. Чтобы Claude их собрал, отправьте экспорт: Настройки → Экспорт.', 'Episode tasks come with a pack. To get them, send Claude an export: Settings → Export.')}</div>`;
  return { title: sh.title, back: true, sec: 'media', pill: esc(sh.current || ''), sub: L('Сериал', 'Series'), body: h };
}

/* ---------- Speaking ---------- */
function vSpeaking() {
  const list = (S.speaking || []).slice().sort((a, b) => (b.date + (b.at || '')).localeCompare(a.date + (a.at || '')));
  const last = list[0], sm = last && speakSum(last);
  let h = `<div class="hero glow"><div class="big2"><b>${last ? shortDur(daysSince(last.date)) : '—'}</b>${sm && sm.level ? `<span class="tagx">${esc(sm.level)}</span>` : ''}</div>
    <div class="meta" style="justify-content:flex-start">${last ? L('с последнего разговора', 'since the last talk') + (sm.turns ? ' · ' + sm.turns + ' ' + P(sm.turns, 'реплика', 'реплики', 'реплик', 'turn', 'turns') : '') : L('Разговоров пока нет', 'No talks yet')}</div>
    ${sm && sm.errors.length ? `<div class="meta" style="justify-content:flex-start;margin-top:14px">${L('Чаще всего', 'Most frequent')}</div><div class="tagrow">${sm.errors.map(e => `<span class="tagx">${esc(e.c)} ×${e.n}</span>`).join('')}</div>` : ''}
    ${ctaHtml('speak-new', '', L('Вставить отчёт', 'Paste report'), '', '', IC.plus)}</div>`;
  const f = S.speakFocus;
  if (f && (f.items || []).length) h += groupHead(L('Фокус следующего разговора', 'Focus for the next talk')) + `<div class="group fitems">${f.items.map(x => `<div>${esc(x)}</div>`).join('')}</div>`;
  if (list.length) h += groupHead(L('Разговоры', 'Talks') + ' · ' + list.length) + '<div class="group">' + list.map(r => {
    const s = speakSum(r);
    return `<div class="row static" style="align-items:flex-start"><span class="row-main">
      <span class="row-sub">${fmtShort(r.date)}${s.check ? ' · ' + L('контрольная', 'level check') : ''}${s.turns ? ' · ' + s.turns + ' ' + P(s.turns, 'реплика', 'реплики', 'реплик', 'turn', 'turns') : ''}</span>
      ${s.topics ? `<span class="row-title" style="display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${esc(s.topics)}</span>` : ''}
      ${s.errors.length ? `<span class="row-sub">${L('Ошибки: ', 'Mistakes: ')}${esc(s.errors.map(e => e.c + ' ×' + e.n).join(' · '))}</span>` : ''}
      ${s.train.length ? `<span class="row-sub">${L('Тренировать: ', 'Practise: ')}${esc(s.train.join('; '))}</span>` : ''}
      <span><button class="link-btn" data-act="speak-del" data-id="${esc(r.id)}">${UI.speakDel === r.id ? L('Точно удалить?', 'Delete for sure?') : L('Удалить', 'Delete')}</button></span>
    </span>${s.level ? `<span class="tagx">${esc(s.level)}</span>` : ''}</div>`;
  }).join('') + '</div>';
  h += `<div class="gfoot">${L('Не входит в план дня. День с разговором засчитывается в серию. Полный отчёт уходит в экспорт для Claude.', 'Not part of the daily plan. A day with a talk counts towards your streak. The full report goes into the export for Claude.')}</div>`;
  return { title: L('Говорение', 'Speaking'), back: true, sec: 'speaking', sub: L('Голосом в чате Speaking · по желанию', 'By voice in the Speaking chat · optional'), body: h };
}
