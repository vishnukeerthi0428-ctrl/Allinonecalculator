// Render the assembled HTML to PDF with Mermaid diagrams, bookmarks, header/footer.
// Usage: node render_pdf.js <in.html> <out.pdf> <mermaid.min.js> "<header text>"
const { chromium } = require("playwright");
(async () => {
  const [html, out, mjs, header, mode] = process.argv.slice(2);
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1500, height: 1000 } });
  await p.goto("file://" + html, { waitUntil: "load" });
  const n = await p.$$eval("pre.mermaid", (els) => els.length);
  if (n) {
    await p.addScriptTag({ path: mjs });
    await p.evaluate(async () => {
      mermaid.initialize({
        startOnLoad: false, theme: "neutral", securityLevel: "strict",
        flowchart: { useMaxWidth: false, rankSpacing: 18, nodeSpacing: 24, padding: 6, wrappingWidth: 260 },
        themeVariables: { fontSize: "17px" },
        er: { useMaxWidth: false }, state: { useMaxWidth: false }, sequence: { useMaxWidth: false },
      });
      const W = 1030, H = 665; let k = 0;
      const dims = (svg) => { const m = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/); return m ? [+m[3], +m[4]] : [W, H]; };
      for (const pre of [...document.querySelectorAll("pre.mermaid")]) {
        const code = pre.textContent; const re = /^(\s*(?:flowchart|graph)\s+)(TD|TB|LR|RL|BT)/;
        const variants = re.test(code) ? [code.replace(re, "$1TD"), code.replace(re, "$1LR")] : [code];
        let best = null;
        for (const v of variants) {
          try { const r = await mermaid.render("m" + (k++), v); const [w, h] = dims(r.svg); const sc = Math.min(W / w, H / h); if (!best || sc > best.sc) best = { sc, svg: r.svg }; }
          catch (e) { best = best || { sc: 0, svg: "<pre>Diagram error: " + e.message + "</pre>" }; }
        }
        const wrap = document.createElement("div"); wrap.className = "mermaid-wrap"; wrap.innerHTML = best.svg;
        const svg = wrap.querySelector("svg");
        if (svg) { svg.removeAttribute("height"); svg.setAttribute("width", "100%"); svg.style.maxWidth = "100%"; svg.style.maxHeight = "176mm"; }
        pre.replaceWith(wrap);
      }
    });
  }
  await p.pdf({
    path: out, format: "A4", landscape: true, printBackground: true, outline: true, tagged: false,
    margin: { top: "14mm", bottom: "16mm", left: "12mm", right: "12mm" }, displayHeaderFooter: true,
    headerTemplate: `<div style="font-size:7pt;width:100%;display:flex;justify-content:space-between;padding:0 12mm;color:#666"><span>${header}</span><span>Confidential · v1.1 · 28 Nov 2026</span></div>`,
    footerTemplate: mode === "nofooter" ? `<span></span>` : `<div style="font-size:7pt;width:100%;text-align:center;color:#666">Page <span class=pageNumber></span> of <span class=totalPages></span></div>`,
  });
  await browser.close();
  console.log(out + " (" + n + " diagrams)");
})();
