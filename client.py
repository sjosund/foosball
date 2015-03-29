from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import json
import random
from time import sleep


class SlowSquareClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        for i in range(10000):
            x = 10. * random.random()
            self.sendMessage(json.dumps(x).encode('utf8'))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            res = json.loads(payload.decode('utf8'))
            self.sendClose()

    def onClose(self, wasClean, code, reason):
        if reason:
            print(reason)
        reactor.stop()


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://localhost:9000", debug=False)
    factory.protocol = SlowSquareClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
