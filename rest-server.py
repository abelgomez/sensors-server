#! /usr/bin/env python3

import os
import tornado.ioloop
import tornado.web
import time
import json
import datetime
import Adafruit_DHT
import argparse
from threading import Thread

DEFAULT_TYPE = 22
DEFAULT_INTERVAL = 10
DEFAULT_PORT = 8080

TYPE = os.getenv('SS_TYPE', DEFAULT_TYPE)
INTERVAL = os.getenv('SS_INTERVAL', DEFAULT_INTERVAL)
PORT = os.getenv('SS_PORT', DEFAULT_PORT)
LABEL = os.getenv('SS_LABEL')

parser = argparse.ArgumentParser(description='REST server to publish information about local sensors.')
parser.add_argument('-b', '--bcm',
                    required=True,
                    type=int,
                    help='GPIO pin to liste to.')
parser.add_argument('-t', '--type',
                    default=TYPE,
                    type=int,
                    help='DHT variant (11 or 22). May also be set using the SS_TYPE environment variable.')
parser.add_argument('-i', '--interval',
                    default=INTERVAL,
                    type=int,
                    help='Refresh interval. May also be set using the SS_INTERVAL environment variable.')
parser.add_argument('-p', '--port',
                    default=PORT,
                    type=int,
                    help='Port to deploy the web service. May also be set using the SS_PORT environment variable.')
parser.add_argument('-l', '--label',
                    default=LABEL,
                    help='Label identifying this sensor. May also be set using the SS_LABEL environment variable.')

args = parser.parse_args()

BCM = args.bcm
TYPE = args.type
INTERVAL = args.interval
PORT = args.port
LABEL = args.label

class DhtXX:

    def __init__(self):
        if args.label is not None:
            self.label = LABEL
        self.type = TYPE
        self.refresh_interval = INTERVAL
        self.last_update = None
        self.temperature = None
        self.humidity = None

        self.__update()
        thread = Thread(target=self.__update_loop, args=(self,))
        thread.setDaemon(True)
        thread.start()

    def __update(self):
        self.last_update = str(datetime.datetime.now())
        (h, t) = Adafruit_DHT.read_retry(self.type, BCM)
        if t is not None:
            self.temperature = round(t,1)
        if h is not None:
            self.humidity = round(h,1)

    def __update_loop(self, data):
        while True:
            data.__update()
            time.sleep(self.refresh_interval)

class dhtxx(tornado.web.RequestHandler):
    def get(self):
        format = self.get_argument('output', 'json')
        if format == 'json':
            self.write(dhtxx.__dict__)
        elif format == 'raw-temperature':
            self.write("{0:.1f}".format(dhtxx.temperature))
        elif format == 'raw-humidity':
            self.write("{0:.1f}".format(dhtxx.humidity))
        else:
            self.write('Invalid argument')

application = tornado.web.Application([
        (r"/api/dht", dhtxx),
])

dhtxx = DhtXX()

if __name__ == "__main__":
    application.listen(PORT, "0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
