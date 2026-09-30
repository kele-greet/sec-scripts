import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({"User-Agent":"Day1-Lab/1.0(authorized-text-ony)"})

try:
    resp = session.get("https://example.com" ,timeout=(3.05,5))
    resp.encoding = resp.apparent_encoding
    print(resp.status_code,len(resp.text))
    soup = BeautifulSoup(resp.text,"html.parser")
    print("title:",soup.title.string.strip() if soup.title else None)
    print("links:",[a.get("herf") for a in soup.find_all("a")])
except requests.RequestException as exc:
    print(f"网络不可用，跳过在线演示:{type(exc).__name__}:{exc}")
    
HTML = """<html><head><title>靶场后台</title></head>
<body><a href="/admin">管理</a><a href="/login">登录</a></body></html>"""
soup =BeautifulSoup(HTML,"html.parser")
print(soup.title.string)
print([a["href"] for a in soup.select("a")])