from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
fail=[]
try:
 with sync_playwright() as p:
  edge=Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe");browser=p.chromium.launch(**({"executable_path":str(edge)} if edge.exists() else {}),headless=True)
  for file in sorted(root.glob("*.html")):
   page=browser.new_page()
   errs=[]
   page.on("pageerror",lambda e:errs.append(str(e)))
   try:
    resp=page.goto(f"http://127.0.0.1:{server.server_port}/{file.name}",wait_until="domcontentloaded",timeout=15000)
    page.wait_for_timeout(250)
    if resp.status!=200 or errs:fail.append((file.name,resp.status,errs[:2]))
    print(file.name,resp.status,"JS_ERRORS",len(errs))
   except Exception as e:fail.append((file.name,str(e)[:160]))
   page.close()
  browser.close()
finally:server.shutdown()
print("TOTAL",len(list(root.glob("*.html"))),"FAILURES",len(fail))
for item in fail:print("FAIL",item)
raise SystemExit(bool(fail))
