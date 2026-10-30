// Cloudflare Worker: DeepL translation proxy for "Мой учебный план".
// The DeepL key is stored as a Worker secret (DEEPL_KEY) and never reaches the app or GitHub.
// Only the app's own site may call it.
const ALLOWED = ['https://kseniyara2020.github.io'];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const ok = ALLOWED.includes(origin);
    const cors = {
      'Access-Control-Allow-Origin': ok ? origin : ALLOWED[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };
    const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json; charset=utf-8' } });

    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (request.method !== 'POST') return json({ error: 'Use POST' }, 405);
    if (!ok) return json({ error: 'Origin not allowed' }, 403);
    if (!env.DEEPL_KEY) return json({ error: 'DEEPL_KEY secret is missing' }, 500);

    let text = '';
    try { text = String((await request.json()).text || '').trim(); } catch (e) {}
    if (!text) return json({ error: 'Empty text' }, 400);
    if (text.length > 500) return json({ error: 'Text is longer than 500 characters' }, 400);

    // Free/Developer keys usually end with ":fx" and use api-free; if the endpoint is wrong, DeepL answers 403 — then try the other one.
    const hosts = env.DEEPL_KEY.endsWith(':fx') ? ['https://api-free.deepl.com', 'https://api.deepl.com'] : ['https://api.deepl.com', 'https://api-free.deepl.com'];
    const call = host => fetch(host + '/v2/translate', {
      method: 'POST',
      headers: { 'Authorization': 'DeepL-Auth-Key ' + env.DEEPL_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: [text], source_lang: 'EN', target_lang: 'RU' }),
    });
    let r = await call(hosts[0]);
    if (r.status === 403) r = await call(hosts[1]);
    let data = {};
    try { data = await r.json(); } catch (e) {}
    if (!r.ok) return json({ error: (data && data.message) || ('DeepL HTTP ' + r.status) }, r.status === 456 ? 429 : 502);
    return json({ ru: data.translations[0].text });
  },
};
