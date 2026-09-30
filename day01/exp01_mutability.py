import copy
a=(1,2,3)
b=a
a +=(4,)#实际创建了新的a对象然后进行了重新绑定
print(a,b,a is b) #预期出现（1，2，3，4）（1，2，3）False b没变
x = [1,2,3]
y=x
x +=[4]
print(x,y, x is y)#预期出现（1，2，3，4）（1，2，3）True y没变 
p = [1,2,3]; q=[1,2,3]; r=p
print( p == q,p is q,p is r)
s1 = "hello"; s2 = "hello"
print(s1 is s2) #预期出现true(字符串驻留，实现细节)

inner = [1,2,3]
shallow = copy.copy([inner,"x"])
deep = copy.deepcopy([inner,"x"])
inner.append(999)
print(shallow)
print(deep)
print(shallow[0] is inner,deep[0] is inner) #预期出现 turefalse
print(0.1+0.2,0.1+0.2==0.3)
import math
print(math.isclose(0.1+0.2,0.3))
