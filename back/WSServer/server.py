
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import json
import WSServer.commands as commands
from config import *
from .db import Db
import logging
import asyncio
import threading
import traceback


lock = threading.Lock()
db = Db(lock)


class Handler(WebSocketServerProtocol):
    def __init__(self):
        WebSocketServerProtocol.__init__(self)
        self.temp = db
        self.user = None
        self.user_id = None
        self.user_stat = {}
        self.game = None
        self.channel = self.temp.main_channel
        self.user_rights = 0
        self.addr = None
        self.typing = False
        self.channel.join(self)
        self.logger = logging.getLogger('WSServer')

    def ws_send(self, message):
        self.sendMessage(message.encode('utf-8'), False)

    def get_information(self):
        return {
            'user': self.user,
            'user_id': self.user_id,
            'user_rights': self.user_rights,
            'user_stat': self.user_stat
        }

    def onConnect(self, request):
        self.temp.handlers.append(self)
        self.addr = request.peer[4:]
        self.logger.info('%s Connected' % self.addr)

    def onOpen(self):
        self.ws_send(json.dumps({
            'type': 'welcome',
            'data': {
                'message': 'online-games websocket server WELCOME!',
                'version': VERSION
            }
        }))

    def onMessage(self, payload, is_binary):
        try:
            message = json.loads(payload.decode('utf-8'))
            message_type = message['type']
            data = message['data']
        except (UnicodeDecodeError, ValueError):
            message_type = 'error'
            data = 'Error'
        try:
            message_type = message_type.replace('__', '')
            message_type = message_type.lower()
            self.logger.info('%s Request %s  %s' % (self.addr, message_type, data))
            resp = getattr(commands, message_type)(self, data)
        except Exception as ex:
            resp = {'type': message_type + '_error', 'data': str(ex)}
            self.logger.error('%s Error %s  %s' % (self.addr, message_type, str(ex)))
        self.ws_send(json.dumps(resp))
        self.logger.info('%s Response  %s  %s' % (self.addr, resp['type'], resp['data']))

    def onClose(self, *args):
        commands.leave(self, None)
        if self.channel:
            self.channel.leave(self)
        self.temp.handlers.remove(self)
        self.logger.info('%s Disconnected' % (self.addr,))


class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def run(secret_key):
    form = '[%(asctime)s]  %(levelname)s: %(message)s'
    logger = logging.getLogger("WSServer")
    logging.basicConfig(level=logging.INFO, format=form)

    log_handler = logging.FileHandler('logs/log.txt')
    log_handler.setFormatter(logging.Formatter(form))

    logger.addHandler(log_handler)
    logger.info('Start %s:%s' % (IP, PORT))

    Handler.secret_key = secret_key
    factory = WebSocketServerFactory(u"ws://%s:%s" % (IP, PORT))
    factory.protocol = Handler

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, IP, PORT)
    loop.run_until_complete(coro)

    thread = Thread(loop.run_forever)
    return thread


if __name__ == '__main__':
    sk = 'shouldintermittentvengeancearmagainhisredrighthandtoplagueus'
    run(sk)
    while True:
        try:
            out = eval(input())
            if out is not None:
                print(out)
        except:
            traceback.print_exc()
