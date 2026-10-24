from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",headless=True)
  page=browser.new_page()
  page.goto(f"http://127.0.0.1:{server.server_port}/vault.html")
  page.wait_for_function("document.querySelectorAll('#donation-methods h3').length===3")
  names=page.locator("#donation-methods h3").all_inner_texts()
  addresses=page.locator("#donation-methods code").all_inner_texts()
  assert any("Bitcoin" in n for n in names)
  assert any("Ethereum" in n for n in names)
  assert any("PayPal" in n for n in names)
  assert len(addresses)==2
  print("PASS donation options:",names,"PUBLIC_ADDRESSES",len(addresses))
  browser.close()
finally:server.shutdown()
