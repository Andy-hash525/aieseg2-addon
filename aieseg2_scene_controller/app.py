import os
import requests
import traceback
import time
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt

# ===== MQTT設定 =====
MQTT_HOST = "core-mosquitto"
MQTT_PORT = 1883

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASSWORD")

# ===== AiSEG2 =====
HOST = "http://192.168.0.216"
session = requests.Session()

MQTT_TOPIC = "aiseg/scene/#"


# ===== token取得 =====
def get_token():
    try:
        r = session.get(HOST, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        el = soup.select_one("#token")
        return el.get("token") if el else None
    except Exception as e:
        print("[ERROR] token:", e)
        return None


# ===== シーン実行 =====
def run_scene(scene_no):
    token = get_token()
    if not token:
        print("[ERROR] no token")
        return

    url = f"{HOST}/action/devices/device/32i21"

    data = {
        "ctrlType": "1",
        "sceneNo": str(scene_no),
        "token": token
    }

    try:
        res = session.post(url, data=data, timeout=5)
        print(f"[OK] scene {scene_no} ({res.status_code})")
    except Exception as e:
        print("[ERROR] scene:", e)


# ===== MQTT =====
def on_message(client, userdata, msg):
    try:
        scene = int(msg.payload.decode())
        run_scene(scene)
    except Exception as e:
        print("[ERROR] mqtt:", e)


def on_connect(client, userdata, flags, rc):
    print("[MQTT] connected:", rc)
    client.subscribe(MQTT_TOPIC)


# ===== main =====
def main():
    print("=== AiSEG2 Add-on Starting ===")

    client = mqtt.Client()

    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
    except Exception as e:
        print("[FATAL] MQTT:", e)
        return

    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[FATAL]", e)
        traceback.print_exc()
        while True:
            time.sleep(10)