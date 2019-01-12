#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
import time
import json
import datetime
import Adafruit_DHT
from threading import Thread


GPIO_SENSOR = 23
INTERVAL = 10
LISTEN=8080

class DhtXX:

    def __init__(self):
        self.type = Adafruit_DHT.DHT22
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
