import Pipe
from random import choice,randint
def get_pipe():
    if not randint(0,9):
        return Pipe.XPipe if randint(0,1) else Pipe.X2Pipe
    else:
        return Pipe.BPipe if randint(1,5)>2 else Pipe.SPipe