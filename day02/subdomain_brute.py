import argparse
import http.client
import random
import socket
import ssl
import string
import sys
from concurrent.futures import ThreadPoolExecutor,as_completed

UA = "subdomain-brute-lab/1.0"

WORDS = ["www","mail","api","dev","test","admin","blog","static","cdn","git","vpn","db","monitor"]

def resolve(name,timeout=3.0):
    """DNS 解析，返回IP列表为空"""
    old = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        infos = socket.getaddrinfo(name,None)
    except (socket.gaierror,socket.timeout,OSError):
        return []
    finally:
        socket.setdefaulttimeout(old)
    return sorted({i[4][0] for i in infos})
def probe_http(host,timeout=5.0):
    for schema in ("https","http"):
        conn = None
        try:
            if schema == "https":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                conn = http.client.HTTPSConnection(host,443,timeout=timeout,context=ctx)
            else: 
                conn = http.client.HTTPConnection(host,80,timeout=timeout)
            conn.request("GET","/",headers={"User-Agent":UA,"Connection":"close"})
            resp = conn.getresponse()
            resp.read(1)
            return schema,resp.status
        except Exception:
            continue
        finally:
            if conn:
                conn.close()
    return None

def scan_one(sub,domain,bashline,timeout):
    fqdn = f"{sub}.{domain}"
    ips = resolve(fqdn,timeout)
    if not ips:
        return None
    if bashline and set(ips) == set(bashline):
        return None
    r = probe_http(fqdn,timeout)
    return fqdn,ips,r

def main():
    ap =argparse.ArgumentParser()
    ap.add_argument("-d","--domain",required=True)
    ap.add_argument("-w","--wordlist")
    ap.add_argument("-t","--threads",type=int,default=30)
    ap.add_argument("-timeout",type=float,default=3.0)
    args = ap.parse_args()
    
    
    words = open(args.wordlist).read().split() if args.wordlist else WORDS
    
    probe_name = "".join(random.choices(string.ascii_lowercase,k=12)) + "."+ args.domain
    
    baseline = resolve(probe_name)
    print(f"[*]tartget={args.domain} words={len(words)} baseline ={baseline or '无'}")
    
    with ThreadPoolExecutor(args.threads) as pool:
        futs = [pool.submit(scan_one,w,args.domain,baseline,args.timeout) for w in words]
        
        for f in as_completed(futs):
            r = f.result()
            if r:
                fqdn,ips,http = r
                print(f"[+]{fqdn:40s}{ips[0]}:16s{http or '-'}")
                
                
if __name__=="__main__":
    main()