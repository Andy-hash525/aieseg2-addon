import requests
import time
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt

HOST = "http://192.168.0.216"

session = requests.Session()


# --- token取得 ---
def get_token():
    r = session.get(HOST)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select_one("#token")["token"]


# --- シーン実行 ---
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


# --- MQTT ---
def on_message(client, userdata, msg):
    try:
        scene = int(msg.payload.decode())
        run_scene(scene)
    except Exception as e:
        print("error:", e)


def main():
    client = mqtt.Client()

    client.connect("core-mosquitto", 1883, 60)
    client.subscribe("aiseg/scene/#")

    client.on_message = on_message

    print("AiSEG2 addon started")
    client.loop_forever()


if __name__ == "__main__":
    main()