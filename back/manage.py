from WSServer import server
import traceback
import sys
import os

sys.path.append(os.getcwd() + '/WSServer/')


if __name__ == '__main__':
    sk = 'shouldintermittentvengeancearmagainhisredrighthandtoplagueus'
    server.run(sk)
    while True:
        try:
            out = eval(input())
            if out is not None:
                print(out)
        except:
            traceback.print_exc()
