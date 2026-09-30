def bad_box(item,box=[]):
    box.append(item)
    return box
def good_box(item,box=None):
    if box is None:
        box = []
    box.append(item)
    return box
def immutable_degault(item,tag="default"):
    return f"{tag}:{item}"
print(bad_box(1),bad_box(2),bad_box(3))
print(good_box(1),good_box(3),good_box(3))
print(bad_box.__defaults__)
def mutate(nums):
    nums.append(999)
def rebind(nums):
    nums=[0]
a = [1,2,3]
mutate(a);print(a)
b = [1,2,3]
rebind(b);print(b)

def build_requst(method,url,*headers,timeout=5, ** options):
    return{
        "method": method, "url":url,
        "header": tuple(headers), "timeout":timeout, "options":options,
    }
print(build_requst("GET","http://t/", "A:1", "B:2",timeout=3,verify=False,proxies=None))
args = ("POST","http://t/api")
kw = { "timeout":1,"data":"x=1"}
print(build_requst(*args, **kw)["options"])
def scan(host,/,port,*,treads=100):
    return f"{host}:{port} threads={treads}"
print(scan("127.0.0.1",port=80))



        