import base64,json,hashlib
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
R=Path(__file__).resolve().parents[1]
private=ec.derive_private_key(0x519B423D715F8B581F4FA8EE59F4771A5B44C8130B4E3EACCA54A56DDA72B464,ec.SECP256R1())
n=private.public_key().public_numbers();b64=lambda x:base64.urlsafe_b64encode(x.to_bytes(32,'big')).decode().rstrip('=')
jwk={'kty':'EC','crv':'P-256','x':b64(n.x),'y':b64(n.y)}
payload={'protocol':'agent-stopover-passport-v2','challenge_id':'vector-1','answer':'portable UTF-8: café','nonce':'fixed-public-test-nonce','public_key':jwk}
canonical=json.dumps(payload,separators=(',',':'),ensure_ascii=False).encode();der=private.sign(canonical,ec.ECDSA(hashes.SHA256()));r,s=decode_dss_signature(der);raw=r.to_bytes(32,'big')+s.to_bytes(32,'big')
vector={'source_runtime':'Python cryptography 50.0.2','payload':payload,'canonical_utf8_hex':canonical.hex(),'public_jwk_fingerprint_sha256':hashlib.sha256(json.dumps(jwk,separators=(',',':')).encode()).hexdigest(),'signature_base64':base64.b64encode(raw).decode()}
(R/'passport-conformance-vector.json').write_text(json.dumps(vector,indent=2,ensure_ascii=False)+'\n')
