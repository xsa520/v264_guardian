import time
import datetime
import json
import os
import requests

BOT_TOKEN = "你的Bot Token"
CHAT_ID = "你的Chat ID"

# 檔案名稱
STATUS_FILE = "account_status.json"

# 預設值
account_status = {
    "total_assets": 10000,
    "total_trades": 0,
    "successful_trades": 0,
    "total_profit": 0
}

# 載入歷史資料
def load_account_status():
    global account_status
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            account_status = json.load(f)
        print("✅ 成功載入上次紀錄")
    else:
        print("⚠️ 沒有找到舊資料，從初始設定開始")

# 儲存最新資料
def save_account_status():
    with open(STATUS_FILE, "w") as f:
        json.dump(account_status, f)

# 送出推播
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

# 監控主程式
def monitor():
    global account_status
    load_account_status()  # 啟動時載入紀錄

    while True:
        now = datetime.datetime.utcnow()

        # 每天檢查一次（如果有異常才推播）
        try:
            response = requests.get("https://google.com", timeout=10)
            if response.status_code != 200:
                send_message(f"⚠️【警報】API異常！狀態碼：{response.status_code}")
        except Exception as e:
            send_message(f"❗【緊急警報】無法連線至目標服務：{e}")

        # 每週一 UTC 0點推送總資產報告
        if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
            message = (
                f"📊【本週資產報告】\n"
                f"總資產：{account_status['total_assets']} 美元\n"
                f"交易次數：{account_status['total_trades']} 次\n"
                f"累計利潤：{account_status['total_profit']} 美元\n"
            )
            send_message(message)
            time.sleep(60)  # 防止周報重複推播

        save_account_status()  # 每天保存一次最新資產資料
        time.sleep(86400)  # 每天檢查一次

if __name__ == "__main__":
    monitor()
