"""
port_scanner.py --- Day1 多线程tcp端口扫描器
用法：python3 port_sacnner.py -t 127.0.0.1 -p 1-1024 -w 200 -T 0.5
只做tcp connect探测
"""
"""import argparse
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
def parse_ports(spec):
    ports = set()
    for part in spec.split(","):
        if "-" in part :
            a,b = part.split("-")
            ports.update(range(int(a),int(b)+1))
        else:
            ports.add(int(part))
    return sorted(ports)
def scan(host,port,timeout=0.5):
    s= socket.socket()
    s.settimeout(timeout)
    try:
        return port, s.connect_ex((host,port)) == 0
    finally:
        s.close()
def main(host,port_spec,workers=200):
    ports = parse_ports(port_spec)
    open_ports=[]
    with ThreadPoolExecutor(workers) as pool:
        futures = [pool.submit(scan,host,p) for p in ports]
        for f in as_completed(futures):
            port,ok = f.result()
            if ok:
                open_ports.append(port)
                print(f"[+]{port} open")
    return sorted(open_ports)
if __name__ == "__main__":
    main("127.0.0.1","1-1024")"""


import socket
from concurrent.futures import ThreadPoolExecutor,as_completed

def chuli_port(p):
    ports = set ()
    for part in p.split(","):
        if "-" in part:
            a,b = part.split("-")
            ports.update(range(int(a),int(b)+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def scan_start (host,port,timeout=0.5):
    s = socket.socket()
    s.settimeout(timeout)
    try: 
        return port,s.connect_ex((host,port)) == 0
    finally:
        s.close()
def main (host ,post_list,workers=200):
    ports = chuli_port(post_list)
    open_ports = []
    with ThreadPoolExecutor(workers) as pool:
        futures = [pool.submit(scan_start,host,p)for p in ports]
        for f in as_completed(futures):
            port,ok = f.result()
            if ok:
                open_ports.append(port)
                print(f"[+]{port}open")
        return sorted(open_ports)

if __name__ =="__main__":
    main("127.0.0.1","1-1000")
    