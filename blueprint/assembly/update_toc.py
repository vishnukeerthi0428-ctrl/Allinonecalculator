"""Populate TOC fields in a .docx using LibreOffice (headless UNO), keeping .docx format.
Usage: soffice-python update_toc.py <in.docx>   (run via the bundled LibreOffice python)"""
import sys, time, subprocess, uno
from com.sun.star.beans import PropertyValue
def pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p
path = sys.argv[1]
proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                         '--accept=socket,host=127.0.0.1,port=2002;urp;'])
ctx = None
for _ in range(60):
    try:
        local = uno.getComponentContext()
        res = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        ctx = res.resolve("uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception:
        time.sleep(1)
desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
url = uno.systemPathToFileUrl(path)
doc = desktop.loadComponentFromURL(url, "_blank", 0, (pv("Hidden", True),))
idx = doc.getDocumentIndexes()
n = idx.getCount()
for i in range(n):
    idx.getByIndex(i).update()
doc.refresh()
doc.storeToURL(url, (pv("FilterName", "MS Word 2007 XML"),))
doc.close(True)
try:
    desktop.terminate()
except Exception:
    pass
proc.wait(timeout=60)
print("TOC updated:", n, "index(es)")
