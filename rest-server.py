#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
import time
import json
import datetime
import Adafruit_DHT
import argparse
from threading import Thread

parser = argparse.ArgumentParser(description='Shutdown button listener')
parser.add_argument('-b', '--bcm',
                    required=True,
                    type=int,
                    help='GPIO pin to liste to')
parser.add_argument('-t', '--type',
                    default=22,
                    type=int,
                    help='DHT variant (11 or 22)')
parser.add_argument('-i', '--interval',
                    default=10,
                    type=int,
                    help='Refresh interval')
parser.add_argument('-p', '--port',
                    default=8080,
                    type=int,
                    help='Port to deploy the web service')

args = parser.parse_args()

GPIO_SENSOR = args.bcm
INTERVAL = args.interval
LISTEN = args.port
TYPE = args.type

class DhtXX:

    def __init__(self):
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
        (h, t) = Adafruit_DHT.read_retry(self.type, GPIO_SENSOR)
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
    application.listen(LISTEN, "0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
