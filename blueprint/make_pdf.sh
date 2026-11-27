#!/usr/bin/env bash
# Usage: blueprint/make_pdf.sh <markdown-file> "<header label>"
set -euo pipefail
MD="$1"; LABEL="${2:-Application Blueprint}"
DIR="$(cd "$(dirname "$0")" && pwd)"; BASE="${MD%.md}"; HTML="$(mktemp --suffix=.html)"
pandoc "$MD" -s --metadata title="$LABEL" -c "$DIR/.pdf-style.css" --embed-resources -o "$HTML"
node -e "
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://$HTML');await p.pdf({path:'$BASE.pdf',format:'A4',landscape:true,printBackground:true,
margin:{top:'14mm',bottom:'16mm',left:'12mm',right:'12mm'},displayHeaderFooter:true,
headerTemplate:'<div style=\"font-size:7pt;width:100%;text-align:right;padding-right:12mm;color:#666\">AI Growth Engine — $LABEL</div>',
footerTemplate:'<div style=\"font-size:7pt;width:100%;text-align:center;color:#666\">Page <span class=pageNumber></span> of <span class=totalPages></span></div>'});await b.close();})()"
rm -f "$HTML"; echo "$BASE.pdf"
