import socket
import ssl
import sys

CRLF = "\r\n"

def build_request(method,path,host,body=""):
    if isinstance(body,str):
        body =body.encode()
    lines = [
        f"{method} {path} HTTP/1.1",
        f"Host:{host}",
        "User-Agent: raw-http-lab/1.0",
        "Connection: close",
        f"Content-Length:{len(body)}",
    ]
    head =CRLF.join(lines) + CRLF +CRLF
    return head.encode() + body


def send(host,port,payload,use_tls=False):
    s =  socket.create_connection((host,port),timeout=8)
    if use_tls:
        ctx =ssl.create_default_context()
        s =ctx.wrap_socket(s,server_hostname=host)
    s.sendall(payload)
    data = b""
    while chunk :=s.recv(4096):
        data +=chunk
    s.close()
    return data
def explain(resp:bytes):
    head,_,body= resp.partition(b"\r\n\r\n")
    lines = head.split(b"\r\n")
    
    print(f"[状态行]{lines[0].decode(errors='replace')}")
    for line in lines[1:]:
        if line:
            print(f"[头]{line.decode(errors="replace")}")
        print("[空行]   CRLF CRLF —— 头到此结束")
        print(f"[body]{len(body)}字节")
        print(body[:300].decode(errors="replace"))
if __name__=="__main__":
    if len(sys.argv) < 3:
        print("用法:python http_raw.py <host><path>[--tls]")
        sys.exit(1)
    host,path = sys.argv[1],sys.argv[2]
    use_tls = "--tls" in sys.argv[3:]
    port = 443 if use_tls else 80
    payload = build_request("GET",path,host)
    print(f"===发出的baowen{len(payload)}===")
    print(payload.decode(errors="replace").replace("\r\n","\\r\\n\n"))
    
    resp = send(host,port,payload,use_tls)
    print(f"\n===响应====")
    explain(resp)
    
    
    