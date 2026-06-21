#!/usr/bin/with-contenv bashio

MQTT_USER=$(bashio::config 'mqtt_user')
MQTT_PASSWORD=$(bashio::config 'mqtt_password')

export MQTT_USER
export MQTT_PASSWORD

python3 /app.py