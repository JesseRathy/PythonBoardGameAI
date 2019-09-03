import ChessVar as Game2
from GameTreeSearch import minimax
import time as time

b = Game2.ChessVar(None, player='W')
b.display()
bSuccessors = b.successors()
b.testBoard()
b.testBoard2()
"""
for i in bSuccessors:
    print()
    print()
    print()
    i.display()
    a = i.successors()
    for k in a:
        print()
        print()
        print()
        k.display()
        a1 = k.successors()
        for j in a1:
            print()
            print()
            print()
            j.display()
"""