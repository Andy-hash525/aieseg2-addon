import os
import time
import requests
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt

MQTT_HOST = "core-mosquitto"
MQTT_PORT = 1883

MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASS = os.getenv("MQTT_PASSWORD", "")

MQTT_TOPIC = "aiseg/scene/#"

HOST = "http://192.168.0.216"
session = requests.Session()


def get_token():
    try:
        r = session.get(HOST, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        el = soup.select_one("#token")
        return el.get("token") if el else None
    except:
        return None


def run_scene(scene_no):
    token = get_token()
    if not token:
        print("no token")
        return

    url = f"{HOST}/action/devices/device/32i21"

    data = {
        "ctrlType": "1",
        "sceneNo": str(scene_no),
        "token": token
    }

    session.post(url, data=data)
    print("scene:", scene_no)


def on_message(client, userdata, msg):
    scene = int(msg.payload.decode())
    run_scene(scene)


def on_connect(client, userdata, flags, rc):
    print("MQTT connected:", rc)
    client.subscribe(MQTT_TOPIC)


def main():
    print("=== START ===")

    client = mqtt.Client()

    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
