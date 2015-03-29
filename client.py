from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import json
import random
from time import sleep

import sys

from twisted.python import log
from twisted.internet import reactor
import argparse

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


    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://{}:{}".format(args.ip, args.port), debug=False)
    factory.protocol = SlowSquareClientProtocol

    reactor.connectTCP(args.ip, args.port, factory)
    reactor.run()
