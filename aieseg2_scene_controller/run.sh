#!/usr/bin/with-contenv bashio

export MQTT_USER=$(bashio::config 'mqtt_user')
export MQTT_PASSWORD=$(bashio::config 'mqtt_password')

python3 /app.py