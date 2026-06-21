#!/usr/bin/with-contenv bashio

echo "RUN.SH STARTED"

MQTT_USER=$(bashio config 'mqtt_user')
MQTT_PASSWORD=$(bashio config 'mqtt_password')

echo "MQTT_USER=$MQTT_USER"

export MQTT_USER
export MQTT_PASSWORD

python3 /app/app.py
