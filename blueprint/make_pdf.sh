#!/usr/bin/env bash
# Usage: blueprint/make_pdf.sh <markdown-file> "<header label>"
# Renders Markdown (with ```mermaid blocks) to an A4-landscape PDF.
# Needs: pandoc, node + playwright, and blueprint/.tools/mermaid.min.js
#   (fetch once: npm i mermaid@11.4.1 && cp node_modules/mermaid/dist/mermaid.min.js blueprint/.tools/)
set -euo pipefail
export LANG=C.UTF-8 LC_ALL=C.UTF-8
MD="$1"; LABEL="${2:-Application Blueprint}"
DIR="$(cd "$(dirname "$0")" && pwd)"; BASE="$(cd "$(dirname "$MD")" && pwd)/$(basename "${MD%.md}")"
HTML="$(mktemp --suffix=.html)"
pandoc "$MD" -s --metadata title="$LABEL" -c "$DIR/.pdf-style.css" --embed-resources -o "$HTML"
HTML="$HTML" OUT="$BASE.pdf" LABEL="$LABEL" MJS="$DIR/.tools/mermaid.min.js" node -e '
const {chromium}=require("playwright");(async()=>{
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1500,height:1000}});
await p.goto("file://"+process.env.HTML);
const n=await p.$$eval("pre.mermaid",els=>els.length);
if(n){await p.addScriptTag({path:process.env.MJS});
 await p.evaluate(async()=>{
   mermaid.initialize({startOnLoad:false,theme:"neutral",securityLevel:"strict",flowchart:{useMaxWidth:false,rankSpacing:18,nodeSpacing:24,padding:6,wrappingWidth:260,diagramPadding:4},themeVariables:{fontSize:"17px"},er:{useMaxWidth:false},state:{useMaxWidth:false},sequence:{useMaxWidth:false}});
   const W=1030,H=665; let k=0;
   const dims=svg=>{const m=svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);return m?[+m[3],+m[4]]:[W,H];};
   for(const pre of [...document.querySelectorAll("pre.mermaid")]){
     const code=pre.textContent; const re=/^(\s*(?:flowchart|graph)\s+)(TD|TB|LR|RL|BT)/;
     const variants=re.test(code)?[code.replace(re,"$1TD"),code.replace(re,"$1LR")]:[code];
     let best=null;
     for(const v of variants){try{const r=await mermaid.render("m"+(k++),v);const [w,h]=dims(r.svg);
       const sc=Math.min(W/w,H/h); if(!best||sc>best.sc) best={sc,svg:r.svg};}catch(e){best=best||{sc:0,svg:"<pre>Diagram error: "+e.message+"</pre>"};}}
     const wrap=document.createElement("div");wrap.className="mermaid-wrap";wrap.innerHTML=best.svg;
     const svg=wrap.querySelector("svg"); if(svg){svg.removeAttribute("height");svg.setAttribute("width","100%");svg.style.maxWidth="100%";svg.style.maxHeight="176mm";}
     pre.replaceWith(wrap);}
 });
 const bad=await p.$$eval(".mermaid-wrap",els=>els.filter(e=>!e.querySelector("svg")).length);
 if(bad) console.error("WARNING: "+bad+" mermaid diagram(s) failed to render");}
await p.pdf({path:process.env.OUT,format:"A4",landscape:true,printBackground:true,
 margin:{top:"14mm",bottom:"16mm",left:"12mm",right:"12mm"},displayHeaderFooter:true,
 headerTemplate:`<div style="font-size:7pt;width:100%;text-align:right;padding-right:12mm;color:#666">AI Growth Engine — ${process.env.LABEL}</div>`,
 footerTemplate:`<div style="font-size:7pt;width:100%;text-align:center;color:#666">Page <span class=pageNumber></span> of <span class=totalPages></span></div>`});
await b.close();console.log(process.env.OUT+" ("+n+" diagrams)");})()'
rm -f "$HTML"
