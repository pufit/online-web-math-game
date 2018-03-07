from WSServer import server
import traceback


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
