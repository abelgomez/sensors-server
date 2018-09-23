#! /usr/bin/env bash

INSTDIR=/opt/sensors
SVCS_LOCATION=/etc/systemd/system/

[ "$(whoami)" != "root" ] && exec sudo -p "[sudo] This script must be executed as root. Password for %p: " -- "$0" "$@"

systemctl stop sensors-server
systemctl disable sensors-server
rm $SVCS_LOCATION/sensors-server.service
rm $INSTDIR/rest-server.py
rmdir $INSTDIR


