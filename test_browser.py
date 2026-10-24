from pathlib import Path
from playwright.sync_api import sync_playwright
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
root=Path(__file__).resolve().parent
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
url=f"http://127.0.0.1:{server.server_port}/"
try:
 with sync_playwright() as p:
  edge=Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe");browser=p.chromium.launch(**({"executable_path":str(edge)} if edge.exists() else {}),headless=True)
  page=browser.new_page()
  errors=[]
  page.on("pageerror",lambda e:errors.append(str(e)))
  page.goto(url+"self-test.html")
  page.locator("#run").click()
  page.wait_for_function("document.querySelectorAll('#results li').length===24",timeout=15000)
  print("SELFTEST",page.locator("#summary").inner_text())
  print("FAILURES",page.locator(".fail").all_inner_texts())
  page.goto(url+"arcade.html")
  page.wait_for_function("document.querySelectorAll('article').length===6",timeout=10000)
  print("ARCADE",page.locator("#status").inner_text(),"CARDS",page.locator("article").count())
  page.locator("article").first.locator("textarea").fill("CG-2047 GBP 148.50 2026-11-15")
  page.locator("article").first.locator("button").click()
  print("ARCADE_CHECK",page.locator("article").first.locator("[data-feedback]").inner_text())
  print("SCORE",page.locator("#score").inner_text())
  print("JS_ERRORS",errors[:10])
  browser.close()
finally:server.shutdown()
