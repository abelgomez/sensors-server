#! /usr/bin/env bash

INSTDIR="/opt/sensors"
SVC_LOCATION="/etc/systemd/system"
SVC_FILE="$SVC_LOCATION/sensors-server.service"
CONF_LOCATION="$SVC_FILE.d"
CONF_FILE="$CONF_LOCATION/override.conf"

[ "$(whoami)" != "root" ] && exec sudo -p "[sudo] This script must be executed as root. Password for %p: " -- "$0" "$@"

systemctl stop sensors-server
systemctl disable sensors-server

rm $SVC_FILE
rm $CONF_FILE
rm $INSTDIR/rest-server.py
rmdir $INSTDIR
rmdir $SVC_LOCATION
rmdir $CONF_LOCATION
