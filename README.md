# REST Server for RPi local sensors

This repository contains a example REST server, based on Tornado, that publishes information on locally mounted sensors.

Currently, a simple [Adafruit DHT22](https://www.adafruit.com/product/385) sensor is supported by the service. A DHT11 sensor may be used too with minimal changes.

Since the DHT sensors are a bit slow, and are not guaranteed to provide a measurement when queried, the service reads the sensor in regular intervals in background to keep an up-to-date value.

# Steps to install and use

*NOTE:* These service and scripts assume a Debian system is used.

1. Clone this repository:

```
git clone https://github.com/abelgomez/sensors-server/
```

2. Set the GPIO pin to which the DHT22 sensor is connected (i.e., edit the `GPIO_SENSOR` constant in the file `rest-server.py`):

```
nano rest-server.py
```

Other constants that can be customized are the read `INTERVAL`, and the port where the server `LISTEN`s.

3. Run the `install.sh` script to install the service under `/opt/sensors`, including any required dependencies and the associated `systemd` service.

```
sudo ./install.sh
```

# Steps to uninstall

1. Run the `uninstall.sh` script.

```
sudo ./uninstall.sh
```

# API

At this moment, the server only supports the Adafruit DHT22 (or its similar DHT11 if the sources are adapted accordingly) sensor, which can be queried as:

```
http://<HOST>:<LISTEN>/api/dht22
```

For example, the query:

```
http://localhost:8080/api/dht22
```

Provides the following result:

```
{
  "humidity": 59.1,
  "temperature": 27.6,
  "last_update": "2018-09-24 13:25:59.979584",
  "refresh_interval": 10
}
```

This query can be customized with an `output` parameter, with the following values:

* `output=json` (default). This query returns the same value as if the query is performed without specifying an output format (see above).

* `output=raw-temperature`. This query (e.g. `http://localhost:8080/api/dht22?output=raw-temperature`) returns only the temperature as a raw value (e.g. `27.6`).

* `output=raw-humidity`. This query (e.g. `http://localhost:8080/api/dht22?output=raw-humidity`) returns only the humidity as a raw value (e.g. `59.1`).

* Any other `output` value returns `Invalid argument`.
