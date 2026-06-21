import os
import paho.mqtt.client as mqtt

MQTT_HOST = "core-mosquitto"
MQTT_PORT = 1883

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASSWORD")

client = mqtt.Client()

if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

client.connect(MQTT_HOST, MQTT_PORT, 60)

# ===== 設定 =====
HOST = "http://192.168.0.216"
MQTT_HOST = "core-mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "aiseg/scene/#"

session = requests.Session()


# ===== token取得 =====
def get_token():
    try:
        r = session.get(HOST, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        el = soup.select_one("#token")

        if not el:
            print("[ERROR] token not found")
            return None

        return el.get("token")

    except Exception as e:
        print("[ERROR] token fetch failed:", e)
        return None


# ===== シーン実行 =====
def run_scene(scene_no):
    token = get_token()

    if not token:
        print("[ERROR] no token, skip")
        return

    url = f"{HOST}/action/devices/device/32i21"

    data = {
        "ctrlType": "1",
        "sceneNo": str(scene_no),
        "token": token
    }

    try:
        res = session.post(url, data=data, timeout=5)
        print(f"[OK] scene {scene_no} executed ({res.status_code})")

    except Exception as e:
        print("[ERROR] scene failed:", e)


# ===== MQTT受信 =====
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode().strip()
        print("[MQTT] received:", payload)

        scene = int(payload)
        run_scene(scene)

    except Exception as e:
        print("[ERROR] message error:", e)


def on_connect(client, userdata, flags, rc):
    print("[MQTT] connected rc:", rc)
    client.subscribe(MQTT_TOPIC)


# ===== メイン =====
def main():
    print("=== AiSEG2 Scene Add-on Starting ===")

    client = mqtt.Client()

    # ★ ここ重要（core-mosquitto接続）
    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
    except Exception as e:
        print("[FATAL] MQTT connect failed:", e)
        return

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()


# ===== 起動 =====
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[FATAL]", e)
        traceback.print_exc()
        while True:
            time.sleep(10)