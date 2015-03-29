from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import json
from twisted.internet.defer import Deferred, \
    inlineCallbacks, \
    returnValue

import sys

from twisted.python import log
from twisted.internet import reactor
import argparse

def sleep(delay):
    d = Deferred()
    reactor.callLater(delay, d.callback, None)
    return d


class SlowSquareServerProtocol(WebSocketServerProtocol):

    @inlineCallbacks
    def slowsquare(self, x):
        if x > 5:
            raise Exception("number too large")
        else:
            yield sleep(1)
            returnValue(x * x)

    @inlineCallbacks
    def onMessage(self, payload, isBinary):
        if not isBinary:
            x = json.loads(payload.decode('utf8'))
            try:
                res = yield 2*x #self.slowsquare(x)
            except Exception as e:
                self.sendClose(1000, "Exception raised: {0}".format(e))
            else:
                self.sendMessage(json.dumps(res).encode('utf8'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    log.startLogging(sys.stdout)


    factory = WebSocketServerFactory(
        "ws://{}:{}".format(args.ip, args.port),
        debug=False
    )
    factory.protocol = SlowSquareServerProtocol

    reactor.listenTCP(args.port, factory)
    reactor.run()
