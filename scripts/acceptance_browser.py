import asyncio, json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.async_api import async_playwright
R = Path(__file__).resolve().parents[1]
server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(R)))
Thread(target=server.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{server.server_port}/"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(bypass_csp=True, viewport={"width": 320, "height": 256})
        page = await context.new_page()
        requests = []
        page.on("request", lambda req: requests.append(req.url))
        await page.goto(BASE + "lounge.html")
        await page.wait_for_timeout(200)
        assert not any("api.github.com" in url or "klaklak.com" in url for url in requests)
        async def fulfill(route):
            url = route.request.url
            if url.endswith("/comments") or "/comments?" in url:
                await route.fulfill(json=[{"body": "a reply that must stay out of the live region"}])
            elif "labels=agent-chat" in url:
                await route.fulfill(json=[{"number": 1, "title": "[Agent Chat] Hello", "body": "issue body", "html_url": "https://github.com/chapelgate/agent-stopover-experiment/issues/1", "comments": 1, "user": {"login": "visitor"}, "created_at": "2026-10-24T00:00:00Z", "state": "open"}, {"number": 2, "title": "[Agent Chat] Pull", "pull_request": {}, "html_url": "https://github.com/chapelgate/agent-stopover-experiment/pull/2", "comments": 0, "user": {"login": "visitor"}, "created_at": "2026-10-24T00:00:00Z", "state": "open"}])
            else:
                await route.fallback()
        await page.route("**/api.github.com/**", fulfill)
        await page.click("#refresh")
        await page.wait_for_selector("article button")
        assert await page.locator("article").count() == 1
        button = page.locator("article button")
        await button.click()
        await page.locator("article [role=status]").filter(has_text="Loaded 1").wait_for()
        assert await button.evaluate("node => node === document.activeElement")
        assert "a reply" not in await page.locator("article [role=status]").inner_text()
        assert "a reply" in await page.locator("article").inner_text()
        await page.click("#load-chat")
        sandbox = await page.locator("#chat-frame iframe").get_attribute("sandbox")
        assert sandbox and "allow-scripts" in sandbox
        for name in ("tools.html", "impossible-gym.html", "toolbox.html", "community.html", "facilities.html", "index.html"):
            await page.set_viewport_size({"width": 320, "height": 256})
            await page.goto(BASE + name)
            assert await page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"), name
        await page.set_viewport_size({"width": 1366, "height": 768})
        await page.goto(BASE + "index.html")
        box = await page.locator("a[href='./toolbox.html']").first.bounding_box()
        assert box and box["y"] + box["height"] < 768, box
        await page.goto(BASE + "collaborate.html")
        assert await page.locator("#title").get_attribute("required") is not None
        assert await page.locator("#details").get_attribute("required") is not None
        assert "*" in await page.locator("label[for=title]").inner_text()
        assert "*" in await page.locator("label[for=details]").inner_text()
        await page.locator("#prepare").click()
        assert await page.locator("#title").evaluate("node => !node.validity.valid")
        requests.clear()
        await page.goto(BASE + "self-test.html")
        assert not any(url.endswith("toolbox.html") for url in requests)
        await page.click("#run")
        await page.locator("#summary").filter(has_text="24 / 24").wait_for()
        assert await page.locator("#summary").inner_text() == "24 / 24 tests passed"
        count = sum(url.endswith("toolbox.html") for url in requests)
        await page.click("#run")
        await page.locator("#summary").filter(has_text="24 / 24").wait_for()
        assert sum(url.endswith("toolbox.html") for url in requests) == count == 1
        blocked = await context.new_page()
        await blocked.route("**/toolbox.html", lambda route: route.abort())
        await blocked.goto(BASE + "self-test.html")
        await blocked.click("#run")
        await blocked.locator("#summary").filter(has_text="Test runner error").wait_for(timeout=8000)
        assert "0 / 24" not in await blocked.locator("#summary").inner_text()
        await blocked.close()
        await page.goto(BASE + "agent-passport.html")
        vector = json.loads((R / "passport-conformance-vector.json").read_text())
        reordered = {"y": vector["payload"]["public_key"]["y"], "extra": True, "x": vector["payload"]["public_key"]["x"], "crv": vector["payload"]["public_key"]["crv"], "kty": vector["payload"]["public_key"]["kty"]}
        match = await page.evaluate("""({payload, reordered, hex}) => {
          const text = AgentPassport.canonicalPayload(payload.challenge_id, payload.answer, payload.nonce, reordered);
          return [...new TextEncoder().encode(text)].map(v => v.toString(16).padStart(2, '0')).join('') === hex;
        }""", {"payload": vector["payload"], "reordered": reordered, "hex": vector["canonical_utf8_hex"]})
        assert match
        await page.click("#generate")
        await page.locator("#sign").wait_for()
        for _ in range(40):
            if not await page.locator("#sign").is_disabled():
                break
            await page.wait_for_timeout(100)
        else:
            raise AssertionError("sign stayed disabled")
        body = await page.locator("body").inner_text()
        fields = await page.locator("input,textarea").evaluate_all("nodes => nodes.map(node => node.value)")
        assert '"d"' not in body and all('"d"' not in value for value in fields)
        await page.click("#forget-key")
        assert await page.locator("#sign").is_disabled()
        await page.goto(BASE + "facilities.html")
        good = json.loads((R / "checkpoint-template.json").read_text())
        await page.set_input_files("#checkpoint-import", {"name": "checkpoint.json", "mimeType": "application/json", "buffer": json.dumps(good).encode()})
        await page.locator("#checkpoint-status").filter(has_text="restored").wait_for()
        await page.fill("#checkpoint-next", "changed")
        async with page.expect_download() as download_info:
            await page.click("#checkpoint-download")
        exported = json.loads(Path(await (await download_info.value).path()).read_text())
        assert exported["next_step"] == "changed"
        assert all(exported[key] == good[key] for key in good if key != "next_step")
        await page.set_input_files("#checkpoint-import", {"name": "bad.json", "mimeType": "application/json", "buffer": b'{"schema_version":"2.0","next_step":"nope"}'})
        await page.locator("#checkpoint-status").filter(has_text="Import failed").wait_for()
        assert await page.locator("#checkpoint-next").input_value() == "changed"
        await page.goto(BASE + "noticeboard.html")
        await page.locator("#updates section").first.wait_for()
        await page.fill("#seen", "1")
        async with page.expect_download() as seen_info:
            await page.click("#export")
        seen_path = await (await seen_info.value).path()
        await page.set_input_files("#import", seen_path)
        await page.locator("#status").filter(has_text="later updates").wait_for()
        await page.goto(BASE + "results.html")
        blocks = await page.locator('script[type="application/ld+json"]').all_text_contents()
        assert any(json.loads(block).get("@type") == "Dataset" for block in blocks)
        await page.emulate_media(reduced_motion="reduce")
        await page.goto(BASE + "facilities.html")
        assert await page.evaluate("getComputedStyle(document.documentElement).scrollBehavior === 'auto'")
        await page.goto(BASE + "toolbox.html")
        assert await page.locator("#output").get_attribute("tabindex") == "0"
        await page.goto(BASE + "tool-storage.html")
        verdicts = await page.evaluate("""() => ({
          local: AgentCatalogue.safeUrl('./toolbox.html'),
          flagged: AgentCatalogue.safeUrl('https://example.org/a', true, ['https://example.org']),
          script: AgentCatalogue.safeUrl('javascript:alert(1)'),
          data: AgentCatalogue.safeUrl('data:text/plain,x'),
          file: AgentCatalogue.safeUrl('file:///tmp/x'),
          scheme: AgentCatalogue.safeUrl('//evil.example/x'),
          external: AgentCatalogue.safeUrl('https://example.org/a', false, ['https://example.org'])
        })""")
        assert verdicts["local"] and verdicts["flagged"]
        assert all(verdicts[key] is None for key in ("script", "data", "file", "scheme", "external"))
        for name in ("index.html", "invite.html", "lounge.html", "vault.html", "collaborate.html"):
            await page.goto(BASE + name)
            ratio = await page.evaluate("""() => {
              const probe = document.querySelector('button, a.button, a.action, section');
              const style = getComputedStyle(probe);
              const parse = value => value.match(/\\d+/g).map(Number);
              const transparent = value => !value || value === 'transparent' || /,\\s*0\\s*\\)/.test(value);
              let node = probe.parentElement;
              while (node && transparent(getComputedStyle(node).backgroundColor)) node = node.parentElement;
              const adjacent = getComputedStyle(node || document.body).backgroundColor;
              const channel = value => { const c = value / 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
              const lum = rgb => 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2]);
              const left = lum(parse(style.borderTopColor)), right = lum(parse(adjacent));
              return (Math.max(left, right) + 0.05) / (Math.min(left, right) + 0.05);
            }""")
            assert ratio >= 3, (name, ratio)
        strict = await browser.new_context(viewport={"width": 800, "height": 600})
        probe = await strict.new_page()
        notes = []
        probe.on("console", lambda msg: notes.append(msg.text) if "Refused to" in msg.text else None)
        for name in ("index.html", "lounge.html", "toolbox.html", "vault.html", "agent-passport.html", "facilities.html"):
            await probe.goto(BASE + name)
        assert not notes, notes[:5]
        await probe.goto(BASE + "csp-probe.html")
        await probe.click("#probe")
        assert await probe.locator("#probe").inner_text() == "probe"
        await browser.close()
        print("Chromium acceptance tests passed")
    server.shutdown()

asyncio.run(main())
