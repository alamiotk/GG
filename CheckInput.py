import os
import sys
# Windows
if os.name == 'nt':
    import msvcrt
# Posix (Linux, OS X)
else:
    from select import select
    
def kbhit():
    if os.name == 'nt':
        return msvcrt.kbhit()
    
    else:
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []

def CheckInput():
    if kbhit():
        return sys.stdin.readline().strip()
    return ""