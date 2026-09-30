"""import re
import sys
from collections import Counter
LOG_RE = re.compile(
    r'(?P<ip>\S+) \S+ \S+[(?P<time>[^\]]+)\]'
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+|-)'
)

RULES ={
    "SQL注入":  re.compile(r"(?i)(union\s+select|sleep\(|information_schema|'\s*or\s*'?1)"),
    "XSS":     re.compile(r"(?i)(<script|javascript:|onerror\s*=|alert\()"),
    "路径穿越": re.compile(r"(\.\./|/etc/passwd|win\.ini)"),
    "命令注入": re.compile(r"(?i)(;\s*(cat|id|whoami)\b|\|\s*id\b|%3b)"),
    "文件包含": re.compile(r"(?i)(php://|file://|data://)"),
    "扫描器":   re.compile(r"(?i)(sqlmap|nikto|nmap|dirbuster|gobuster|wpscan)"),
}

def parse(line):
    m = LOG_RE.match(line.strip())
    if not m:
        return None
    g = m.groupdict()
    attacks = [name for name,pat in RULES.items() if pat.search(line)]
    return{
        "ip":g["ip"],
        "method":g["method"],
        "path":g["path"],
        "status":int(g["status"]),
        "size":0 if g["size"] == "-" else int(g["size"]),
        "attacks":attacks,
    }

def analyze(lines):
    entries = [e for e in (parse(ln) for ln in lines ) if e]
    if not entries:
        print("[x]无效的日志行")
        return
    ips = Counter(e["ip"] for e in entries)
    codes = Counter(e["status"] for e in entries)
    paths = Counter(e["path"].split("?")[0] for e in entries)
    atks = Counter(a for e in entries for a in e["attacks"])
    
    print(f"有效行：{len(entries)}")
    print(f"独立 IP： {len(ips)}")
    print(f"Top IP : {ips.most_common(5)}")
    print(f"状态码:{dict(codes)}")
    print(f"top攻击路径{paths.most_common(5)}")
    print(f"攻击路径:{dict(atks)}")
    bad = {e['ip'] for e in entries if e["attacks"]}
    print(f"ip keyi:{bad}")
if __name__ == "__main__":
    with open(sys.argv[1],encoding="utf-8",errors="replace") as f:
        analyze(f.readlines())"""
        
import re
import sys
from collections import Counter

LOG_RE = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+|-)'
)

RULES = {
    "SQL注入":  re.compile(r"(?i)(union\s+select|sleep\(|information_schema)"),
    "XSS":     re.compile(r"(?i)(<script|javascript:|onerror\s*=|alert\()"),
    "路径穿越": re.compile(r"(\.\./|/etc/passwd|win\.ini)"),
    "命令注入": re.compile(r"(?i)(;\s*(cat|id|whoami)\b|\|\s*id\b|%3b)"),
    "文件包含": re.compile(r"(?i)(php://|file://|data://)"),
    "扫描器":   re.compile(r"(?i)(sqlmap|nikto|nmap|dirbuster|gobuster|wpscan)"),
}


def parse(line):
    m = LOG_RE.match(line.strip())
    if not m:
        return None
    g = m.groupdict()
    attacks = [name for name, pat in RULES.items() if pat.search(line)]
    return {
        "ip": g["ip"],
        "method": g["method"],
        "path": g["path"],
        "status": int(g["status"]),
        "size": 0 if g["size"] == "-" else int(g["size"]),
        "attacks": attacks,
    }


def analyze(lines):
    entries = [e for e in (parse(ln) for ln in lines) if e]
    if not entries:
        print("[x] 无有效日志行")
        return

    ips = Counter(e["ip"] for e in entries)
    codes = Counter(e["status"] for e in entries)
    paths = Counter(e["path"].split("?")[0] for e in entries)
    atks = Counter(a for e in entries for a in e["attacks"])

    print(f"有效行: {len(entries)}")
    print(f"独立 IP: {len(ips)}")
    print(f"Top IP: {ips.most_common(5)}")
    print(f"状态码: {dict(codes)}")
    print(f"Top 路径: {paths.most_common(5)}")
    print(f"攻击特征: {dict(atks)}")

    bad = {e["ip"] for e in entries if e["attacks"]}
    print(f"可疑 IP: {bad}")


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        analyze(f.readlines())