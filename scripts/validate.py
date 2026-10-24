import json, re, sys
from pathlib import Path
from xml.etree import ElementTree
root = Path(__file__).resolve().parents[1]
errors = []
for path in root.rglob("*.json"):
    if ".git" in path.parts:
        continue
    try:
        json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{path.name}: {exc}")
try:
    ElementTree.parse(root / "sitemap.xml")
except Exception as exc:
    errors.append(f"sitemap.xml: {exc}")
methods = json.loads((root / "donation-methods.json").read_text())["methods"]
for method in methods:
    if (method["status"] != "active" or method["owner_verified"] is not True) and method["destination"] is not None:
        errors.append(f"unsafe donation {method['id']}")
facilities = json.loads((root / "facilities.json").read_text())
for facility in facilities["facilities"]:
    for action in facility.get("actions", []):
        if any(verb in action for verb in ("submit", "propose", "report", "post", "reply")):
            detail = facility.get("action_details", {}).get(action, {})
            if detail.get("provider") != "GitHub" or detail.get("visibility") != "public" or detail.get("requires_login") is not True:
                errors.append(f"unsafe action {facility['id']}:{action}")
htmls = [path for path in root.glob("*.html") if path.name != "wallet-setup.html"]
base = "https://chapelgate.github.io/agent-stopover-experiment/"
for path in htmls:
    text = path.read_text()
    if text.count('rel="canonical"') != 1:
        errors.append(f"{path.name}: canonical count")
    expected = base if path.name == "index.html" else base + path.name
    if f'href="{expected}"' not in text:
        errors.append(f"{path.name}: canonical target")
    if "<style" in text or "unsafe-inline" in text:
        errors.append(f"{path.name}: inline style or unsafe CSP")
    if re.search(r'<script(?![^>]*\bsrc=)(?![^>]*type="application/ld\+json")', text):
        errors.append(f"{path.name}: inline script")
    if "assets/site-v1.css" not in text:
        errors.append(f"{path.name}: shared css missing")
    for tag in re.findall(r'<a\b[^>]*target="_blank"[^>]*>', text, re.I):
        rel = re.search(r'rel="([^"]*)"', tag, re.I)
        if not rel or not {"noopener", "noreferrer"} <= set(rel.group(1).split()):
            errors.append(f"{path.name}: unsafe target blank")
urls = [node.text for node in ElementTree.parse(root / "sitemap.xml").getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
if len(urls) != len(set(urls)) or any(not url.startswith(base) for url in urls):
    errors.append("sitemap URL invariant")
joined = "\n".join(urls)
if "wallet-setup.html" in joined:
    errors.append("wallet redirect is in the sitemap")
print(f"validated {sum(1 for path in root.rglob('*.json') if '.git' not in path.parts)} JSON files, {len(htmls)} HTML pages and sitemap.xml")
if errors:
    print("\n".join(errors))
    sys.exit(1)
