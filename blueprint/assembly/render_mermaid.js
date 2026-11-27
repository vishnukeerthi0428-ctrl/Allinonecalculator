// Render Mermaid diagrams to PNG files (for the .docx build).
// Usage: node render_mermaid.js <jobs.json> <outDir> <mermaid.min.js>
// jobs.json: [{ "id": "d001", "code": "flowchart TD ..." }, ...]
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const [jobsFile, outDir, mjs] = process.argv.slice(2);
  const jobs = JSON.parse(fs.readFileSync(jobsFile, "utf8"));
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 2 });
  await page.setContent("<!doctype html><html><body style='margin:0;background:#fff'><div id='host'></div></body></html>");
  await page.addScriptTag({ path: mjs });
  await page.evaluate(() => {
    mermaid.initialize({
      startOnLoad: false, theme: "neutral", securityLevel: "strict",
      flowchart: { useMaxWidth: false, rankSpacing: 18, nodeSpacing: 24, padding: 6, wrappingWidth: 260 },
      themeVariables: { fontSize: "17px" },
      er: { useMaxWidth: false }, state: { useMaxWidth: false }, sequence: { useMaxWidth: false },
    });
  });
  let failed = 0;
  for (const job of jobs) {
    const res = await page.evaluate(async ({ code, id }) => {
      const W = 1030, H = 665;
      const re = /^(\s*(?:flowchart|graph)\s+)(TD|TB|LR|RL|BT)/;
      const variants = re.test(code) ? [code.replace(re, "$1TD"), code.replace(re, "$1LR")] : [code];
      let best = null, k = 0;
      for (const v of variants) {
        try {
          const r = await mermaid.render(id + "_" + (k++), v);
          const m = r.svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);
          const w = m ? +m[3] : W, h = m ? +m[4] : H;
          const sc = Math.min(W / w, H / h);
          if (!best || sc > best.sc) best = { sc, svg: r.svg, w, h };
        } catch (e) { if (!best) best = { err: String(e.message || e) }; }
      }
      if (!best || best.err) return { ok: false, err: best ? best.err : "no render" };
      const host = document.getElementById("host");
      host.innerHTML = best.svg;
      const svg = host.querySelector("svg");
      svg.removeAttribute("style");
      svg.setAttribute("width", Math.round(best.w));
      svg.setAttribute("height", Math.round(best.h));
      return { ok: true };
    }, job);
    if (!res.ok) { failed++; console.error("FAILED " + job.id + ": " + res.err); continue; }
    const el = await page.$("#host svg");
    await el.screenshot({ path: path.join(outDir, job.id + ".png"), omitBackground: false });
  }
  await browser.close();
  console.log(`rendered ${jobs.length - failed}/${jobs.length}`);
  process.exit(failed ? 2 : 0);
})();
