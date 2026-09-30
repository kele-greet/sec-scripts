import socket

CRLF = "\r\n"
HOST, PORT = "127.0.0.1", 8080


def send(raw: bytes, tag: str):
    """发原始字节，打印响应首行"""
    print(f"\n=== {tag} ===")
    print(raw.decode("utf-8", "replace").replace("\r\n", "\\r\\n\n"))
    try:
        s = socket.create_connection((HOST, PORT), timeout=5)
        s.sendall(raw)
        data = b""
        while chunk := s.recv(4096):
            data += chunk
        s.close()
        print("[首行]", data.split(b"\r\n", 1)[0].decode("utf-8", "replace"))
    except socket.timeout:
        print("[超时] 服务端在等我发更多数据")     # ← 关键信号


# 变体 1：正常请求（对照组）
normal = (
    f"GET / HTTP/1.1{CRLF}"
    f"Host: {HOST}:{PORT}{CRLF}"
    f"User-Agent: raw-variants/1.0{CRLF}"
    f"Connection: close{CRLF}"
    f"{CRLF}"
).encode()
send(normal, "变体1 · 正常 GET")


# 变体 2：去掉 Host（HTTP/1.1 里 Host 必需）
no_host = (
    f"GET / HTTP/1.1{CRLF}"
    f"User-Agent: raw-variants/1.0{CRLF}"
    f"Connection: close{CRLF}"
    f"{CRLF}"
).encode()
send(no_host, "变体2 · 没有 Host")
# 严格服务端（nginx/httpbin）→ 400
# 宽松服务端（python -m http.server）→ 200  ← 解析宽松 = Host 攻击的前提


# 变体 3：Content-Length 撒谎（声明 5，实际给 3）
bad_cl = (
    f"POST /post HTTP/1.1{CRLF}"
    f"Host: {HOST}:{PORT}{CRLF}"
    f"Content-Type: application/x-www-form-urlencoded{CRLF}"
    f"Content-Length: 5{CRLF}"
    f"Connection: close{CRLF}"
    f"{CRLF}"
    f"a=1"
).encode()
send(bad_cl, "变体3 · CL 声明 5 实际给 3")
# 服务端挂起等剩余 2 字节 → 超时
# CL 是服务端读 body 的唯一边界，写错就是走私温床


# 变体 4：CL + TE 同时出现（CL.TE 走私探测）
cl_te = (
    f"POST /post HTTP/1.1{CRLF}"
    f"Host: {HOST}:{PORT}{CRLF}"
    f"Content-Length: 4{CRLF}"
    f"Transfer-Encoding: chunked{CRLF}"
    f"Connection: close{CRLF}"
    f"{CRLF}"
    f"1{CRLF}A{CRLF}0{CRLF}{CRLF}"
).encode()
send(cl_te, "变体4 · CL.TE 探测")
# 不同解析器会给出不同结果 → 走私的本质