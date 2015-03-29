from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import json
import random
from time import sleep

import sys

from twisted.python import log
from twisted.internet import reactor
import argparse

import SimpleCV as cv
from ballfinder import ball_position

class BallTracker(WebSocketClientProtocol):
    def onOpen(self):
        cam = cv.Camera(0, prop_set={'width':640, 'heigth':480})
        while True:
            img = cam.getImage()
            x, y = ball_position(img)
            self.sendMessage(json.dumps((x, y)).encode('utf8'))

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
