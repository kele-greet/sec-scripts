import sys
def gen_demo():
    print("gen开始")
    yield 1
    print("gen恢复，产出1")
    yield 2
    print("gen恢复,产出2")
    return "结束标记"
g = gen_demo()
print("创建生成器后什么都没有打印,说明函数体没执行")
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration as exc:
    print("stopIteration.value=",exc.value)

n= 1_000_000
list_obj = [x*x for x in range(n)]
gen_obj = (x*x for x in range(n))
print(f"列表{sys.getsizeof(list_obj):,}字节 vs 生成器 {sys.getsizeof(gen_obj)}")

def iter_lines(path):
    with open(path,"r",encoding="utf-8",errors="replace") as fh:
        for line in fh:
            line =line.rstrip("\n")
            if line:
                yield line
with open("day01/demo.log","w",encoding="utf-8") as fh:
    for i in range(5):
        fh.write(f"line-{i}\n")
print(list(iter_lines("day01/demo.log")))

def numbers():
    for i in range(1,11):
        yield i
pipeline= (n * n for n in numbers() if n%2  ==0)
print(list(pipeline))

class CountDown:
    def __init__(self,start):
        self.current=start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current<=0:
            raise StopIteration
        self.current -=1
        return self.current +1
print(list(CountDown(3)))
print([x for x in CountDown(4)])
g2 = (x for x in range(3))
print(list(g2),list(g2))

print(f"本模块__name_={__name__}")