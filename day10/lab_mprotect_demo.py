import ctypes
from ctypes import wintypes

SHELLCODE = bytes.fromhex("48c7c02A000000c3")  # mov rax,42; ret

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# ---- 常量 ----
MEM_COMMIT  = 0x1000
MEM_RESERVE = 0x2000
MEM_RELEASE = 0x8000
PAGE_READWRITE          = 0x04
PAGE_EXECUTE_READ       = 0x20
PAGE_EXECUTE_READWRITE  = 0x40

# ---- 函数签名（重要！不然 64 位下会截断指针） ----
kernel32.VirtualAlloc.restype  = ctypes.c_void_p
kernel32.VirtualAlloc.argtypes = [
    ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD
]

kernel32.VirtualProtect.restype  = wintypes.BOOL
kernel32.VirtualProtect.argtypes = [
    ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD)
]

# ---- 1. 分配一块 RW 内存 ----
addr = kernel32.VirtualAlloc(
    None, len(SHELLCODE),
    MEM_COMMIT | MEM_RESERVE,
    PAGE_READWRITE,
)
if not addr:
    raise OSError(ctypes.get_last_error(), "VirtualAlloc 失败")
print(f"[1] 已分配 RW 内存 @ {hex(addr)}，此时不可执行")

# ---- 2. 写入 shellcode ----
ctypes.memmove(addr, SHELLCODE, len(SHELLCODE))

# ---- 3. 改成 RX（等价于 mprotect(PROT_READ|PROT_EXEC)）----
old = wintypes.DWORD(0)
ok = kernel32.VirtualProtect(
    ctypes.c_void_p(addr),
    len(SHELLCODE),
    PAGE_EXECUTE_READ,          # 想同时可写就用 PAGE_EXECUTE_READWRITE
    ctypes.byref(old),
)
if not ok:
    raise OSError(ctypes.get_last_error(), "VirtualProtect 失败")
print(f"[2] VirtualProtect(RX) 成功，旧保护 = {hex(old.value)} (应为 0x04 = RW)")

# ---- 4. 调用 shellcode ----
FUNC = ctypes.CFUNCTYPE(ctypes.c_int)
func = FUNC(addr)
result = func()
print(f"[3] 执行流已转移，返回 = {result} (预期 42)")

# ---- 5. “查看 maps”等价：VirtualQuery ----
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress",       ctypes.c_void_p),
        ("AllocationBase",    ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("PartitionId",       wintypes.WORD),
        ("RegionSize",        ctypes.c_size_t),
        ("State",             wintypes.DWORD),
        ("Protect",           wintypes.DWORD),
        ("Type",              wintypes.DWORD),
    ]

mbi = MEMORY_BASIC_INFORMATION()
kernel32.VirtualQuery.restype  = ctypes.c_size_t
kernel32.VirtualQuery.argtypes = [
    ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t
]
kernel32.VirtualQuery(ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi))

prot_names = {
    0x01: "NOACCESS", 0x02: "R", 0x04: "RW",
    0x10: "X", 0x20: "RX", 0x40: "RWX", 0x80: "WC",
}
print(f"[4] VirtualQuery @ {hex(addr)}: "
      f"Protect = {hex(mbi.Protect)} "
      f"({prot_names.get(mbi.Protect, '?')}), "
      f"RegionSize = {hex(mbi.RegionSize)}")

# ---- 6. 释放（好习惯）----
kernel32.VirtualFree.restype  = wintypes.BOOL
kernel32.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD]
kernel32.VirtualFree(ctypes.c_void_p(addr), 0, MEM_RELEASE)