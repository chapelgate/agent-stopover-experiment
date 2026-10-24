import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from jsonschema import Draft202012Validator, FormatChecker
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
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(json.loads((R / instance).read_text()))
donation = json.loads((R / "schemas/donation-methods.schema.json").read_text())
assert list(Draft202012Validator(donation).iter_errors({"methods": [{"id": "x", "status": "active", "owner_verified": False, "destination": "https://bad.example"}]}))
challenge = json.loads((R / "schemas/challenge.schema.json").read_text())
assert list(Draft202012Validator(challenge).iter_errors({"schema_version": "1", "problems": [{"id": "x", "tier": "Warm-up"}]}))
cp = json.loads((R / "checkpoint-template.json").read_text())
out = {**cp, "next_step": "changed"}
assert all(out[k] == cp[k] for k in cp if k != "next_step") and "warning" not in out
checkpoint_schema = json.loads((R / "schemas/checkpoint.schema.json").read_text())
validator = Draft202012Validator(checkpoint_schema, format_checker=FormatChecker())
legacy = {key: value for key, value in cp.items() if key != "resume_destination"}
legacy["schema_version"] = "1.0"
validator.validate(legacy)
assert list(validator.iter_errors({**cp, "resume_destination": "https://evil.example"}))
assert list(validator.iter_errors({key: value for key, value in cp.items() if key != "resume_destination"}))
assert list(validator.iter_errors({**cp, "extra": True}))
assert list(validator.iter_errors({**cp, "task_summary": 7}))
assert list(validator.iter_errors({**cp, "completed_steps": ["x"] * 101}))
assert list(validator.iter_errors({**cp, "next_step": "x" * 8001}))
message_schema = json.loads((R / "schemas/message.schema.json").read_text())
message_validator = Draft202012Validator(message_schema, format_checker=FormatChecker())
message = {"schema_version": "1.0", "kind": "agent-message", "message_id": "reply-1", "thread_id": "thread-1", "in_reply_to": "message-1", "body": "plain data", "created_at_utc": "2026-10-24T12:00:00Z", "acknowledgement": {"message_id": "message-1", "acknowledged": True, "acknowledged_at_utc": "2026-10-24T12:00:00Z"}}
message_validator.validate(message)
assert list(message_validator.iter_errors({**message, "extra": True}))
assert list(message_validator.iter_errors({**message, "acknowledgement": {"message_id": "message-1", "acknowledged": True, "acknowledged_at_utc": None}}))
assert list(message_validator.iter_errors({key: value for key, value in message.items() if key != "acknowledgement"}))
assert list(message_validator.iter_errors({**message, "created_at_utc": "2026-13-99T12:00:00Z"}))
def calendar_true(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = __import__("datetime").datetime.strptime(value.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z" if "." in value else "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return False
    return parsed.strftime("%Y-%m-%dT%H:%M:%S") == value[:19] and parsed.year == int(value[0:4]) and parsed.month == int(value[5:7]) and parsed.day == int(value[8:10])
def ack_matches(value):
    return value["acknowledgement"]["message_id"] == (value["in_reply_to"] or value["message_id"])
assert calendar_true(message["created_at_utc"]) and not calendar_true("2026-02-30T12:00:00Z")
assert ack_matches(message)
bad_ack = {**message, "acknowledgement": {**message["acknowledgement"], "message_id": "other-id"}}
assert not ack_matches(bad_ack)
updates = json.loads((R / "updates.json").read_text())
assert updates["freshness"]["stale_after_days"] == 30 and "not live" in updates["policy"]
assert message["thread_id"] == "thread-1" and message["in_reply_to"] == "message-1" and message["acknowledgement"]["acknowledged"]
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
