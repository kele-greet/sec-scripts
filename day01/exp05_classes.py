from dataclasses import dataclass,field
class Target:
    def __init__ (self,host,port=80):
        self.host=host
        self.port= port
    def __str__(self):
        return f"Target({self.host}:{self.port})"
    def __repr__(self):
        return f"Target(host={self.host!r}, port={self.port!r})"
    def __eq__(self,other):
        if not isinstance(other,Target):
            return NotImplemented
        return (self.host,self.port) == (other.host,other.port)
    def __hash__(self):
        return hash((self.host,self.port))
    
class WebTarget(Target):
    def __init__(self, host, port=80,scheme="http"):
        super().__init__(host,port)
        self.sccheme = scheme
    def __str__(self):
        return f"{self.sccheme}://{super().__str__()}"
t = WebTarget("example.com",443,"https")
print(t)
print(repr(t))
print(isinstance(t,Target), isinstance(t,WebTarget))
print(Target("a",80)== Target("a",80))
print(len({Target("a",80),Target("a",80)}))
class PortList:
    def __init__(self,ports):
        self._prots = list(ports)
    def __len__(self):
        return len(self._prots)
    def __iter__(self):
        return iter(self._prots)
    def __getitem__(self, index):
        return self._prots[index]
    def __contains__(self, item):
        return item in self._prots
pl = PortList([80,443,8080])
print(len(pl),list(pl),pl[1],3306 in pl, [p for p in pl if p >100])

class A:
    def who(self):
        return ["A"]
class B(A):
    def who(self):
        return ["B"] + super().who()
class C(A):
    def who(self):
        return ["c"] + super().who()
class D(B,C):
    def who(self):
        return ["D"]+super().who()
print(D().who())
print([cls.__name__ for cls in D.__mro__])

@dataclass(frozen=True,order=True)
class Finding:
    host:str
    port:int
    service: str = "unknown"
    tags: tuple = field(default_factory=tuple)
f = Finding("1.1.1.1",80,"http",("web",))
print(f)
print(f == Finding("1.1.1.1",80,"http",("web",)))
    
        