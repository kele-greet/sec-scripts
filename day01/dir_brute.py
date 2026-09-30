"""import argparse,random,string,requests
from concurrent.futures import ThreadPoolExecutor,as_completed

S = requests.Session()
S.headers["User-Agent"] = "disbrute"

def probe(base,path,timeout):
    url = base.rstrip("/")+"/"+ path.lstrip("/")
    try:
        r = S.get(url=url,timeout=timeout,allow_redirects=False)
    except requests.RequestException:
        return None
    return path,r.status_code,len(r.content)
def rand_path():
    return "/this_path_should_not_exist_xyz9876"
def main():
    ap= argparse.ArgumentParser()
    ap.add_argument("-u",required=True)
    ap.add_argument("-w",required=True)
    ap.add_argument("-t",type=int,default=20)
    ap.add_argument("-T",type=float,default=5.0)
    a = ap.parse_args()
    
    base = a.u.rstrip("/")
    words = [w.strip() for w in open (a.w,encoding="utf-8") if w.strip() if w.strip() and not w.startswith("#")]
    
    r = S.get(base + rand_path(),timeout=a.T,allow_redirects=False)
    soft = (r.status_code,len(r.content))
    print(f"[*]{base}| {len(words)}words| soft404={soft}")
    
    with ThreadPoolExecutor(a.t) as pool:
        futs = [pool.submit(probe,base,w,a.T)for w in words]
        for f in as_completed(futs):
            res = f.result()
            if not res:
               continue
            _path,code,size=res
            if (code,size) == soft:
                continue
            print(f"[+]{code}{size:>7}B/{_path}")
if __name__=="__main__":
    main()  """
    
import argparse,string,requests,random
from concurrent.futures  import ThreadPoolExecutor,as_completed

S = requests.Session()
S.headers["User-Agent"] = "disbrute"

def probe (base,path,timeout):
    url = base.rstrip("/")+"/"+ path.lstrip("/")
    try:
        r = S.get(url=url,timeout=timeout,allow_redirects=False)
    except requests.RequestException:
        return None
    return path,r.status_code,len(r.content)
def rand_path():
    return "/theisfjisfhisfhsifhsifhs"
def main():
    ap =argparse.ArgumentParser()
    ap.add_argument("-u",required=True)
    ap.add_argument("-w",required=True)
    ap.add_argument("-t",type=int,default=20)
    ap.add_argument("-T",type=float,default=5.0)
    a =ap.parse_args()
    
    base = a.u.rstrip("/")
    words = [w.strip() for w in open (a.w,encoding="utf-8") if w.strip() and not w.startswith("#")]
    
    r = S.get(base+rand_path(),timeout=a.T,allow_redirects=False)
    soft = (r.status_code,len(r.content))
    print(f"[*]{base} | {len(words)}words | soft404 ={soft}")
    with ThreadPoolExecutor(a.t) as pool:
        futs = [pool.submit(probe,base,w,a.T)for w in words]
        for f in as_completed(futs):
            res = f.result()
            if not res:
                continue
            __path_,code,size=res
            if (code,size) ==soft:
                continue
            print(f"[+]{code}{size:>7}B/{__path_}")
if __name__ == "__main__":
    main()
            

    