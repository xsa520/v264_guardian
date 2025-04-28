import time
import requests

BOT_TOKEN = "你的Bot Token"
CHAT_ID = "你的Chat ID"

last_alert_time = 0
last_status = "正常"  # 初始狀態
alert_interval = 1800  # 每1800秒（30分鐘）提醒一次異常

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"發送訊息失敗: {e}")

def monitor():
    global last_alert_time, last_status

    send_message("✅【V26.4軍監系統啟動】已成功啟動，開始巡邏監控中...")  # 開機歡迎推播

    while True:
        try:
            response = requests.get("https://google.com", timeout=10)

            if response.status_code == 200:
                if last_status != "正常":
                    send_message("✅【恢復通知】目標網站已恢復正常！")
                    last_status = "正常"
                    last_alert_time = 0
            else:
                current_time = time.time()
                if last_status == "正常" or (current_time - last_alert_time) > alert_interval:
                    send_message(f"⚠️【警報】目標網站異常！Status Code: {response.status_code}")
                    last_status = "異常"
                    last_alert_time = current_time

        except Exception as e:
            current_time = time.time()
            if last_status == "正常" or (current_time - last_alert_time) > alert_interval:
                send_message(f"❗【緊急警報】無法連線至目標網站：{e}")
                last_status = "異常"
                last_alert_time = current_time

        time.sleep(180)  # 每3分鐘巡邏一次

if __name__ == "__main__":
    monitor()
