import functools
import time
def make_counter():
    n=0
    def inc(step=1):
        nonlocal n
        n += step
        return n
    return inc
c = make_counter()
print(c(),c(5),c())
c = make_counter()
print(c(), c(5),c())
def timer(fn):
    @functools.wraps(fn)
    def wrapper (*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args,**kwargs)
        print(f"[timer] {fn.__name__} ：{(time.perf_counter()-t0)*1000:.2f}ms")
        return result
    return wrapper  

@timer
def sum_range(n):
    return sum(range(n))
print(sum_range(1_000_000), sum_range.__name__, sum_range.__doc__)

def retry (times=3,delay=0.1,exceptions=(Exception,)):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args,**kwargs):
            last_exc = None
            for attempt in range(1,times + 1):
                try:
                    return fn (*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    print(f"[retry] 第{attempt}/{times}次失败:{exc}")
                    if attempt < times:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return deco
_state = {"n":0}
@retry(times=3,delay=0.01,exceptions=(ConnectionError,))
def flaky_connect():
    _state["n"] +=1
    if _state["n"] < 3:
        raise ConnectionError("模拟网络抖动")
    return f"第{_state['n']}次连接成功"
print(flaky_connect())
def deco_a(fn):
    def w(*a,**k):
        print("A前置"); r= fn(*a,**k);print("a后肢"); return r
    return functools.update_wrapper(w,fn)
def deco_b(fn):
    def w(*a,**k):
        print("B前置"); r = fn(*a,**k); print("b后置"); return r
    return functools.update_wrapper(w,fn)
@deco_a
@deco_b
def core():
    print("core 本体")
core()
    