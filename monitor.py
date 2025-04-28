import time
import datetime
import requests

BOT_TOKEN = "你的Bot Token"
CHAT_ID = "你的Chat ID"

weekly_alert_count = 0
continuous_good_weeks = 0
last_status = "正常"
alert_interval = 1800  # 30分鐘防爆推播

last_alert_time = 0  # 上一次異常推播時間記錄

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
    global last_status, last_alert_time, weekly_alert_count, continuous_good_weeks

    send_message("✅【V26.4軍監系統啟動】巡邏中，只推播異常或周報！")

    while True:
        now = datetime.datetime.utcnow()

        # 巡邏偵測區（以 google.com 測試）
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
                    weekly_alert_count += 1

        except Exception as e:
            current_time = time.time()
            if last_status == "正常" or (current_time - last_alert_time) > alert_interval:
                send_message(f"❗【緊急警報】無法連線至目標網站：{e}")
                last_status = "異常"
                last_alert_time = current_time
                weekly_alert_count += 1

        # 每週一 UTC 0點推送巡邏周報
        if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
            if weekly_alert_count == 0:
                continuous_good_weeks += 1
                if continuous_good_weeks >= 2:
                    send_message(f"🏆【連續{continuous_good_weeks}周無異常】V26.4軍監系統表現超卓！")
                else:
                    send_message("✅【本周巡邏報告】巡邏正常，無異常紀錄！")
            else:
                send_message(f"⚠️【本周巡邏報告】本周發生異常 {weekly_alert_count} 次，請注意！")
                continuous_good_weeks = 0  # 遇到異常連續次數歸零

            weekly_alert_count = 0  # 重置本周異常次數
            time.sleep(60)  # 防止周報重複推送，延遲1分鐘後再巡邏

        time.sleep(180)  # 每3分鐘巡邏一次

if __name__ == "__main__":
    monitor()
