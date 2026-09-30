import socket
import sys
import time

def probe (host:str,port:int,timeout:float=2.0) -> None:
    s =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(timeout)
    t0 =time.time()
    code = s.connect_ex((host,port))
    cost = (time.time() - t0) *1000
    if code == 0:
        print(f"[open]{host}:{port}耗时{cost}ms 本地端接口={s.getsockname()[1]}")
        s.close()
    elif code == 111:
        print(f"[close]{host}:{port} 耗时{cost}ms 返回码=1111(ECONNREFUSED)" f"目标fanhuil1rst,说明主机活着但是端口没开")
    else:
        print(f"[FILTER/ERR]{host}:{port} 耗时 {cost:.1f}ms 返回码={code}" f"多半是被fanghuoqianglanjie")



if   __name__ == "__main__":
        host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
        probe(host,port)
        