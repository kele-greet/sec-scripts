import time
from collections import Counter ,defaultdict,deque
data = list (range(200_000))
target = 199_999
t0 = time.perf_counter()
for _ in range(200):
    _ =target in data
t_list =time.perf_counter() - t0
data_set =set (data)
t0 =time.perf_counter()
for _ in range(200):
    _ = target in data_set
t_set = time.perf_counter() - t0
print(f"list in: {t_list*1000:.1f}ms set in : { t_set*1000:.1f}ms")
s = "abcdefg"
print( s[1:5],s[1:5:2],s[::-1],s[-3:],s[100:200])


nums = [1,2,3,4,5,6]
print([n * n for n in nums if n % 2 == 0])
print({n: n*n for n in nums})

matrix =[[1,2],[3,4]]
print([x for row in matrix for x in row])

log_ips = ["1.1.1.1", "2.2.2.2","1.1.1.1","3.3.3.3","1.1.1.1"]
print(Counter(log_ips).most_common(2))
grouped = defaultdict(list)
for ip,port in [("1.1.1.1",80),("1.1.1.1",443),("2.2.2.2",22)]:
    grouped[ip].append(port)
print(dict(grouped))
dq = deque([1,2,3])
dq.appendleft(0);dq.pop()
print(list(dq)) 

def add (item,box=[]):
    box.append(item)
    return box
print(add(1),add(2),add(3))



