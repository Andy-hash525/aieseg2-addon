import subprocess
import time
import requests
import traceback
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt

# =========================
# HA Add-on config取得
# =========================
def config(key):
    try:
        return subprocess.check_output(
            ["bashio", "config", key]
        ).decode().strip()
    except Exception as e:
        print(f"[CONFIG ERROR] {key}:", e)
        return None


# =========================
# MQTT設定
# =========================
MQTT_HOST = "core-mosquitto"
MQTT_PORT = 1883

MQTT_USER = config("mqtt_user")
MQTT_PASS = config("mqtt_password")

MQTT_TOPIC = "aiseg/scene/#"


# =========================
# AiSEG2設定
# =========================
HOST = "http://192.168.0.216"
session = requests.Session()


# =========================
# token取得
# =========================
def get_token():
    try:
        r = session.get(HOST, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        el = soup.select_one("#token")
        return el.get("token") if el else None
    except Exception as e:
        print("[TOKEN ERROR]", e)
        return None


# =========================
# シーン実行
# =========================
def run_scene(scene_no):
    token = get_token()

    if not token:
        print("[ERROR] token not found")
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
        print("[SCENE ERROR]", e)


# =========================
# MQTT受信
# =========================
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode().strip()
        print("[MQTT] received:", payload)

        scene = int(payload)
        run_scene(scene)

    except Exception as e:
        print("[MQTT ERROR]", e)


def on_connect(client, userdata, flags, rc):
    print("[MQTT] connected:", rc)
    client.subscribe(MQTT_TOPIC)


# =========================
# main
# =========================
def main():
    print("=== AiSEG2 Scene Controller START ===")

    print("MQTT_USER:", repr(MQTT_USER))
    print("MQTT_PASS:", repr(MQTT_PASS))

    client = mqtt.Client()

    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    else:
        print("[WARN] MQTT auth not used")

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
    except Exception as e:
        print("[FATAL MQTT CONNECT]", e)
        return

    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[FATAL]", e)
        traceback.print_exc()
        time.sleep(10)
