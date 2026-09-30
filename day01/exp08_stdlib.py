import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

base = Path("day01/out")
base.mkdir(parents=True,exist_ok=True)
report = base / "result.json"
report.write_text('{"ok":true}',encoding="utf-8")
print(report.exists(),report.suffix,list(base.glob("*.json")))

def bulid_parser():
    parser= argparse.ArgumentParser(description="标准库练习脚本")
    parser.add_argument("-t","--target",required=False,default="127.0.0.1")
    parser.add_argument("-p","--ports",default="80,443")
    parser.add_argument("-v","--verbose",action="store_true",help="打开 debug log")
    return parser

args = bulid_parser().parse_args([])
print(args.target,args.ports,args.verbose)

logging.basicConfig(
    level= logging.DEBUG if args.verbose else logging.INFO,
    format= "%(asctime)s[%(levelname)s] %(name)s: %(message)s"
)

log = logging.getLogger("day01")
log.info("日志比print多了级别时间错，来源模块 统一关闭")
log.debug("这一行在-v 时候出现")

IP_RE = re.compile(r"^(?P<a>\d{1,3})\.(?P<b>\d{1,3})\.(?P<c>\d{1,3})\.(?P<d>\d{1,3})$")
m = IP_RE.match("192.168.1.1")
print(m.group("a"),m.groupdict() if m else None)
print(re.findall(r"\d+","alb22c333"))
print(re.sub(r"\s+", " ", " too   many    spaces ").strip())

digest = hashlib.sha256(b"authorized-text-only").hexdigest()
print(digest[:16],len(digest))
result =subprocess.run(["python3","-c","print('clid-ok)"],capture_output=True,text=True,timeout=5)
print(result.returncode,result.stdout.strip())

def square(n):
    return  n*n
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(square,i):i for i in range(6)}
    got = [fut.result() for fut in as_completed(futures)]
print(sorted(got))
print(Counter("abracadabra").most_common(3))
print(sys.version_info[:3])
