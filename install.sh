#! /usr/bin/env bash

INSTDIR=/opt/sensors
SVCS_LOCATION=/etc/systemd/system/

function print() {
  echo "$@";
}

function print_error() {
  echo "ERROR: $@" 1>&2;
}

function check_python3() {
  command -v python3 &> /dev/null
}

function check_pip3() {
  command -v pip3 &> /dev/null
}

function check_module() {
  python3 -c "import $@" &> /dev/null
}

function check_adafruit_dht() {
  check_module "Adafruit_DHT"
}

function check_tornado() {
  check_module "tornado"
}

function yn_question() {
  read -p "$@ [ (Y)es | (N)o | (Q)uit ] " choice
  case "$choice" in
    y|Y ) return 0;;
    n|N ) return 1;;
    q|Q ) exit 1;;
    * ) ;;
  esac
}

[ "$(whoami)" != "root" ] && exec sudo -p "[sudo] This script must be executed as root. Password for %p: " -- "$0" "$@"

if ! check_python3; then
  yn_question "python3 is not installed! Would you like me to run 'apt-get install python3'?" \
    && apt-get install python3
fi

if ! check_pip3; then
  yn_question "pip3 is not installed! Would you like me to run 'apt-get install python-pip3'?" \
    && apt-get install python-pip3
fi

if ! check_adafruit_dht; then
  yn_question "Adafruit_DHT is not installed. Would you like me to run 'pip3 install Adafruit_DHT'?" \
    && pip3 install Adafruit_DHT
fi

if ! check_tornado; then
  yn_question "Adafruit_DHT is not installed. Would you like me to run 'apt-get install python3-tornado'?" \
    && apt-get install python3-tornado
fi

mkdir -p $INSTDIR
cp rest-server.py $INSTDIR
cp sensors-server.service $SVCS_LOCATION

yn_question "Enable and (re)start the sensors REST server?" \
  && systemctl enable sensors-server && systemctl restart sensors-server

