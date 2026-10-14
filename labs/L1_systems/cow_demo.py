"""Copy-on-write demo (complete). Needs Linux/WSL because Windows has no fork().

Run in WSL:  python3 labs/L1_systems/cow_demo.py
Predict first: after the child writes x, what does the parent print?
"""
import os
import sys

if not hasattr(os, "fork"):
    sys.exit("No fork() on this OS. Run inside WSL: wsl python3 labs/L1_systems/cow_demo.py")

x = [0] * 5
pid = os.fork()
if pid == 0:
    x[0] = 99
    print(f"child  pid={os.getpid()} x={x} id(x)={id(x)}")
    os._exit(0)
os.waitpid(pid, 0)
print(f"parent pid={os.getpid()} x={x} id(x)={id(x)}")
print("Same virtual address (id), different physical pages after the write: copy-on-write.")
