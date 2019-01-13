#! /usr/bin/env bash

INSTDIR="/opt/sensors"
SVC_LOCATION="/etc/systemd/system"
SVC_FILE="$SVC_LOCATION/sensors-server.service"
CONF_LOCATION="$SVC_FILE.d"
CONF_FILE="$CONF_LOCATION/override.conf"

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

function create_service_file() {
  cat << EOF > "$SVC_FILE"
[Unit]
Description=REST server providing information about local sensors
After=syslog.target network.target

[Service]
Type=simple
ExecStart=$INSTDIR/rest-server.py --bcm \$GPIO --type \$TYPE

[Install]
WantedBy=multi-user.target
EOF
}

function create_config_file() {
  [ ! -f "$CONF_FILE" ] \
  && mkdir $CONF_LOCATION \
  && cat << EOF > "$CONF_FILE"
[Service]
Environment="GPIO=4"
Environment="TYPE=22"
EOF
}


[ "$(whoami)" != "root" ] && exec sudo -p "[sudo] This script must be executed as root. Password for %p: " -- "$0" "$@"

if ! check_python3; then
  yn_question "python3 is not installed! Would you like me to run 'apt-get install python3'?" \
    && apt-get install python3
fi

if ! check_pip3; then
  yn_question "pip3 is not installed! Would you like me to run 'apt-get install python3-pip'?" \
    && apt-get install python3-pip
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

create_service_file
create_config_file

yn_question "Enable and (re)start the sensors REST server?" \
  && systemctl enable sensors-server && systemctl restart sensors-server

