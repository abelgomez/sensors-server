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

class Dht22:

    def __init__(self):
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
        (h, t) = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, GPIO_SENSOR)
        if t is not None:
            self.temperature = round(t,1)
        if h is not None:
            self.humidity = round(h,1)

    def __update_loop(self, data):
        while True:
            data.__update()
            time.sleep(self.refresh_interval)

class dht22(tornado.web.RequestHandler):
    def get(self):
        format = self.get_argument('output', 'json')
        if format == 'json':
            self.write(dht22.__dict__)
        elif format == 'raw-temperature':
            self.write("{0:.1f}".format(dht22.temperature))
        elif format == 'raw-humidity':
            self.write("{0:.1f}".format(dht22.humidity))
        else:
            self.write('Invalid argument')

application = tornado.web.Application([
        (r"/api/dht22", dht22),
])

dht22 = Dht22()

if __name__ == "__main__":
    application.listen(LISTEN, "0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
