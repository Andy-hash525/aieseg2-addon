import requests
import time
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt

HOST = "http://192.168.0.216"
session = requests.Session()

def get_token():
    r = session.get(HOST)
    soup = BeautifulSoup(r.text, "html.parser")
    el = soup.select_one("#token")
    return el["token"] if el else None

def run_scene(scene_no):
    token = get_token()

    url = f"{HOST}/action/devices/device/32i21"

    data = {
        "ctrlType": "1",
        "sceneNo": str(scene_no),
        "token": token
    }

    session.post(url, data=data)
    print("scene executed:", scene_no)

def on_message(client, userdata, msg):
    scene = int(msg.payload.decode())
    run_scene(scene)

def main():
    client = mqtt.Client()
    client.connect("core-mosquitto", 1883, 60)
    client.subscribe("aiseg/scene/#")
    client.on_message = on_message

    print("started")
    client.loop_forever()

if __name__ == "__main__":
    main()