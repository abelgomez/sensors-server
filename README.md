# REST Server for RPi local sensors

This repository contains a example REST server, based on Tornado, that publishes information on locally mounted sensors.

Currently,  [Adafruit DHT11](https://www.adafruit.com/product/386) and [Adafruit DHT22](https://www.adafruit.com/product/385) sensors are supported by the service.

Since the DHT sensors are a bit slow, and are not guaranteed to provide a measurement when queried, the service reads the sensor in regular intervals in background to keep an up-to-date value.

# Steps to install and use

*NOTE:* These service and scripts assume a Debian system is used.

1. Clone this repository:

```
git clone https://github.com/abelgomez/sensors-server/
```

2. Run the `install.sh` script to install the service under `/opt/sensors`, including any required dependencies and the associated `systemd` service.

```
sudo ./install.sh
```

3. Set the sensor type (DHT11/DHT22) and the GPIO port to listen to in the configuration file:

```
sudo systemctl edit sensors-server.service
```

See other configurable parameters in the [Usage](#usage) section, and adapt the service file `/etc/systemd/system/sensors-server.service` accordingly if needed.

# Usage

```
usage: rest-server.py [-h] -b BCM [-t TYPE] [-i INTERVAL] [-p PORT] [-l LABEL]

REST server to publish information about local sensors.

optional arguments:
  -h, --help            show this help message and exit
  -b BCM, --bcm BCM     GPIO pin to liste to.
  -t TYPE, --type TYPE  DHT variant (11 or 22). May also be set using the
                        SS_TYPE environment variable.
  -i INTERVAL, --interval INTERVAL
                        Refresh interval. May also be set using the
                        SS_INTERVAL environment variable.
  -p PORT, --port PORT  Port to deploy the web service. May also be set using
                        the SS_PORT environment variable.
  -l LABEL, --label LABEL
                        Label identifying this sensor. May also be set using
                        the SS_LABEL environment variable.
```

# Steps to uninstall

1. Run the `uninstall.sh` script.

```
sudo ./uninstall.sh
```

# API

At this moment, the server supports the Adafruit DHT11/DHT22 sensors, which can be queried as:

```
http://<HOST>:<LISTEN>/api/dht
```

For example, the query:

```
http://localhost:8080/api/dht
```

Provides the following result:

```
{
  "temperature": 18.0, 
  "humidity": 34.0, 
  "type": 11, 
  "last_update": "2019-01-13 03:24:13.599569", 
  "refresh_interval": 10,
  "label": "My Server"
}
```

This query can be customized with an `output` parameter, with the following values:

* `output=json` (default). This query returns the same value as if the query is performed without specifying an output format (see above).

* `output=raw-temperature`. This query (e.g. `http://localhost:8080/api/dht22?output=raw-temperature`) returns only the temperature as a raw value (e.g. `27.6`).

* `output=raw-humidity`. This query (e.g. `http://localhost:8080/api/dht22?output=raw-humidity`) returns only the humidity as a raw value (e.g. `59.1`).

* Any other `output` value returns `Invalid argument`.
