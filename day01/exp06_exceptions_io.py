import json
import os
class ToolError(Exception):
    """定义所有异常的基类"""
class NetworkError(ToolError):
    """网络错误"""
class TargetError(ToolError):
    """目标本身不可用(404)"""
class ParseError(ToolError):
    """数据格式错误，输入有问题 """
def divide(a,b):
    try:
        print("try执行")
        result =a/b
    except ZeroDivisionError as exc:
        print(f"excetp:{exc}")
        return "捕获分支返回值"
    else:
        print("esle:无异常正常执行")
        return result
    finally:
        print(f"fially必然执行,即使return")
print(divide(10,2))
print(divide(10,0))

def safe_int(text):
    try:
        return int(text)
    except ValueError:
        return None
    except Exception as exc:
        print(f"没有预料到的错误:{type(exc).__name__}:{exc}")
        return None
print(safe_int("42"),safe_int("abc"),safe_int("1ab"))

os.makedirs("day01",exist_ok=True)
with open("day01/findings.json","w",encoding="utf-8") as fh:
    json.dump({"host": "1.1.1.1","ports":[80,443],"note":"中文部乱码因为encoding"},fh,ensure_ascii=False,indent=2)
with open("day01/findings.json","r",encoding="utf-8") as fh:
    print(json.load(fh)["note"])

class Timer:
    def __enter__(self):
        import time
        self._t0 = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        import time
        print(f"[timer]:{(time.perf_counter()-self._t0)*1000:.2f}ms")
        return False
with Timer():
    sum(range(100000))
def probe(target):
    if target.startswith("http://10."):
        raise TargetError("内部地址,跳过")
    if target == "bad":
        raise NetworkError("连接超时")
    return "ok"
for tg in ["http://1.2.3.4","bad","http://10.0.0.1"]:
    try:
        print(tg,"->",probe(tg))
    except NetworkError:
        print(tg,"-> [可重试网络的问题]")
    except TargetError as exc:
        print(tg,f"->[不可重试]{exc}")
        