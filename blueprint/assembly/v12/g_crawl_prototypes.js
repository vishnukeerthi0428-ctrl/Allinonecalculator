// Group G (R6): sandboxed headless crawl of the V12 HTML prototypes (network disabled).
// Usage: node g_crawl_prototypes.js <website.html> <admin.html> <out.json> [screenshotDir]
const { chromium } = require("playwright");
const fs = require("fs");
const [web, adm, out, shots] = process.argv.slice(2);
const EXTRACT = `(() => {
  const root = document.querySelector('main') || document.body;
  const t = (e) => (e.innerText || e.textContent || '').replace(/\\s+/g, ' ').trim();
  const labelText = (l) => { const c = l.cloneNode(true); c.querySelectorAll('select,textarea,option').forEach(x => x.remove()); return t(c); };
  const fields = [...root.querySelectorAll('input,select,textarea')].map(el => {
    const l = el.closest('label') || (el.id && root.querySelector('label[for="'+el.id+'"]'));
    return { tag: el.tagName.toLowerCase(), type: el.type || '', name: el.name || el.id || '', label: l ? labelText(l).slice(0,90) : (el.getAttribute('aria-label')||el.placeholder||''),
      required: !!el.required, disabled: !!el.disabled, options: el.tagName==='SELECT' ? [...el.options].map(o => t(o)).slice(0, 40) : undefined, nopt: el.tagName==='SELECT'? el.options.length: undefined };
  });
  return {
    title: document.title, lang: document.documentElement.lang, dir: document.documentElement.dir,
    h: [...root.querySelectorAll('h1,h2,h3')].map(e => e.tagName + ':' + t(e).slice(0,120)),
    fields,
    buttons: [...root.querySelectorAll('button')].map(b => ({ text: t(b).slice(0,60), act: b.dataset.act || b.dataset.v6 || b.dataset.v8w || b.dataset.e12 || Object.keys(b.dataset).map(k=>k+'='+b.dataset[k]).join(';').slice(0,60), disabled: b.disabled })),
    tables: [...root.querySelectorAll('table')].map(tb => ({ head: [...tb.querySelectorAll('thead th, tr:first-child th')].map(t).slice(0,20), rows: tb.querySelectorAll('tbody tr').length })),
    details: [...root.querySelectorAll('summary')].map(t).slice(0,40),
    notices: [...root.querySelectorAll('.notice')].map(e => t(e).slice(0,200)).slice(0,10),
    links: [...new Set([...root.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')))].slice(0,80),
    cards: [...root.querySelectorAll('.card h3, .card h2')].map(t).slice(0,60),
    roles: [...root.querySelectorAll('[role]')].map(e => e.getAttribute('role')).filter((v,i,a)=>a.indexOf(v)===i),
    textlen: t(root).length,
    snippet: t(root).slice(0,400)
  };
})()`;
(async () => {
  const browser = await chromium.launch();
  const result = { website: {}, admin: {} };
  for (const [kind, file] of [["website", web], ["admin", adm]]) {
    const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 }, offline: true, javaScriptEnabled: true });
    await ctx.route("**/*", (r) => (r.request().url().startsWith("file:") || r.request().url().startsWith("data:") ? r.continue() : r.abort()));
    const p = await ctx.newPage();
    const errors = []; p.on("pageerror", (e) => errors.push(String(e)));
    await p.goto("file://" + file, { waitUntil: "load" });
    await p.waitForTimeout(500);
    if (kind === "website") {
      const ids = await p.evaluate(() => { const s = new Set(routes.map(r => r.id)); for (let i = 35; i <= 41; i++) s.add('W' + i); return [...s]; });
      result.website.routeMeta = await p.evaluate(() => routes.map(r => ({ id: r.id, name: r.name, kind: r.kind, access: r.access })));
      result.website.chrome = await p.evaluate(() => ({ nav: [...document.querySelectorAll('header nav a, nav a')].map(a => a.textContent.trim() + ' ' + a.getAttribute('href')).slice(0,40),
        footer: [...document.querySelectorAll('footer a')].map(a => a.textContent.trim() + ' ' + a.getAttribute('href')).slice(0,80), langs: typeof V12L !== 'undefined' ? Object.entries(V12L).map(([k,v]) => k + ':' + v.name + ':' + v.dir) : [] }));
      for (const session of ["anon", "demo"]) {
        if (session === "demo") { await p.evaluate(() => { location.hash = 'W21'; }); await p.waitForTimeout(150); const b = await p.$('[data-act="session"]'); if (b) await b.click(); await p.waitForTimeout(200); }
        for (const id of [...ids, "W99X"]) {
          await p.evaluate((id) => { location.hash = id; }, id); await p.waitForTimeout(120);
          result.website[session + ":" + id] = await p.evaluate(EXTRACT);
          if (shots && session === "demo") await p.screenshot({ path: `${shots}/web_${id}.png` });
        }
      }
      // language and RTL check
      await p.evaluate(() => { location.hash = 'W01'; }); await p.waitForTimeout(100);
      for (const l of ["hi", "ar"]) { await p.selectOption('#v12-lang', l).catch(() => {}); await p.waitForTimeout(100); result.website["lang:" + l] = await p.evaluate(() => ({ lang: document.documentElement.lang, dir: document.documentElement.dir, nav: [...document.querySelectorAll('nav a')].map(a => a.textContent.trim()).slice(0, 12) })); }
    } else {
      const ids = await p.evaluate(() => [...DATA.screens.map(s => s.id), 'A089', 'INDEX', 'SERVICES', 'WORKFLOWS', 'RUNS', 'SVC-SM-SVC-01', 'SVC-SM-SVC-05', 'SVC-SM-SVC-09', 'SVC-SM-SVC-10', 'SVC-SM-SVC-17', 'SVC-SM-SVC-28', 'WF-SM-SVC-01-WF01', 'ORG']);
      const uniq = [...new Set(ids)];
      result.admin.audiences = await p.evaluate(() => [...document.querySelectorAll('#persona option')].map(o => o.value));
      result.admin.screenMeta = await p.evaluate(() => DATA.screens.map(s => ({ id: s.id, name: s.name, group: s.group, kind: s.kind, audiences: s.audiences, fields: s.fields, links: s.links, services: s.services, routes: s.routes, tables: s.tables, purpose: s.purpose, originalFields: s.originalFields, additions: s.additions, removal: s.removal })));
      for (const aud of result.admin.audiences) {
        await p.evaluate((a) => { const s = document.getElementById('persona'); s.value = a; s.dispatchEvent(new Event('change', { bubbles: true })); }, aud);
        await p.waitForTimeout(150);
        for (const id of uniq) {
          await p.evaluate((id) => { location.hash = id; }, id); await p.waitForTimeout(60);
          const x = await p.evaluate(EXTRACT); x.aud = aud;
          result.admin[aud + ":" + id] = x;
          if (shots && aud === 'Tenant workspace' && /^(A089|A12|A13|A11|O0|X2|INDEX|RUNS)/.test(id)) await p.screenshot({ path: `${shots}/adm_${id}.png` });
        }
      }
    }
    result[kind].errors = errors;
    await ctx.close();
  }
  fs.writeFileSync(out, JSON.stringify(result));
  await browser.close();
  console.log("done", Object.keys(result.website).length, Object.keys(result.admin).length);
})();
