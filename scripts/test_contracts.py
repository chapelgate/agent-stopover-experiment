import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from jsonschema import Draft202012Validator
R = Path(__file__).resolve().parents[1]
pairs = {
    "facilities.json": "facilities.schema.json",
    "tools.json": "tools.schema.json",
    "impossible-gym.json": "challenge.schema.json",
    "challenge.json": "challenge.schema.json",
    "checkpoint-template.json": "checkpoint.schema.json",
    "donation-methods.json": "donation-methods.schema.json",
    "passport-submission.example.json": "passport-submission.schema.json",
}
for instance, schema_name in pairs.items():
    schema = json.loads((R / "schemas" / schema_name).read_text())
    Draft202012Validator(schema).validate(json.loads((R / instance).read_text()))
donation = json.loads((R / "schemas/donation-methods.schema.json").read_text())
assert list(Draft202012Validator(donation).iter_errors({"methods": [{"id": "x", "status": "active", "owner_verified": False, "destination": "https://bad.example"}]}))
challenge = json.loads((R / "schemas/challenge.schema.json").read_text())
assert list(Draft202012Validator(challenge).iter_errors({"schema_version": "1", "problems": [{"id": "x", "tier": "Warm-up"}]}))
cp = json.loads((R / "checkpoint-template.json").read_text())
out = {**cp, "next_step": "changed"}
assert all(out[k] == cp[k] for k in cp if k != "next_step") and "warning" not in out
base = "https://chapelgate.github.io/agent-stopover-experiment/tool-storage.html"
def safe(value, external=False, allowed=()):
    if not isinstance(value, str) or value.startswith("//"):
        return None
    parsed = urlparse(urljoin(base, value))
    origin = f"{parsed.scheme}://{parsed.netloc}"
    own = "https://chapelgate.github.io"
    if origin == own:
        return parsed.geturl()
    if parsed.scheme == "https" and external and origin in allowed:
        return parsed.geturl()
    return None
assert safe("./toolbox.html") and safe("https://example.org/x", True, ["https://example.org"])
assert all(safe(item) is None for item in ("javascript:alert(1)", "data:text/plain,x", "file:///x", "//evil.example/x"))
tools = json.loads((R / "tools.json").read_text())
ids = [item["id"] for item in tools["contracts"]]
assert len(ids) == len(set(ids)) == 22
print("JSON Schema, negative fixtures, checkpoint roundtrip and URL policy tests passed")
