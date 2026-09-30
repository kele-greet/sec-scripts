import base64
import urllib.parse
import html


def show(title,value):
    print(f"[{title}] {value!r}")


print("===1url 双重编码的绕过===")
raw = " OR 1=1 --"
once = urllib.parse.quote(raw,safe="")
twice = urllib.parse.quote(once,safe="")

show("原文",raw)
show("一次编码",once)
show("两次次编码",twice)
show("解码一次",urllib.parse.unquote(twice))
show("两次次解码",urllib.parse.unquote(urllib.parse.unquote(twice)))

print("\n=== 2.Base64 不是加密 ===")
b = base64.b64encode(b"admin:admin123").decode()
show("原文","admin:admin123")
show("base64",b)
show("还原",base64.b64decode(b).decode())

print("\n === 3.HTML 实体编码 ===")
payload = "<script>alert(1)</script>"
encode = "".join(f"&#x{ord(c):x};" if c in "<>()'\"" else c for c in payload)
show("原文",payload)
show("实体化",encode)
show("还原",html.unescape(encode))

print("\n===4 utf-8 多字节 ===")
for ch in ["a" ,"'" ,"中"]:
    show (f"字符{ch!r}",ch.encode("utf-8").hex())
show("GBK 0xbf5c",bytes.fromhex("bf5c").decode("gbk"))
