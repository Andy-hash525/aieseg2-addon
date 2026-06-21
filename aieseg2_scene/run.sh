#!/bin/bash
set -e

MQTT_USER=$(bashio config 'mqtt_user')
MQTT_PASSWORD=$(bashio config 'mqtt_password')

export MQTT_USER
export MQTT_PASSWORD

echo "MQTT_USER=$MQTT_USER"
echo "MQTT_PASSWORD set: $( [ -n "$MQTT_PASSWORD" ] && echo yes || echo no )"

python3 /app.py