import json
import time
import requests
from datetime import datetime
from futu_api_module import place_order, close_order

# 系統設定
HEARTBEAT_INTERVAL_HOURS = 6
EXTREME_MARKET_THRESHOLD = -1.5
CHECK_INTERVAL_MINUTES = 180
USE_FUTU_API = False
TELEGRAM_TOKEN = '你的Telegram Bot Token'
TELEGRAM_CHAT_ID = '你的Telegram用戶ID'

last_heartbeat_time = 0
defense_mode_active = False
last_restart_time = datetime.utcnow()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram通知失敗: {e}")

def run_monitor():
    send_telegram_message("✅ V27.3 策略已啟動，Telegram 通知測試成功！")
    while True:
        message = "🛡️ V27.3 策略正在監控中... 每10秒推播一次"
        print(message)
        send_telegram_message(message)
        time.sleep(10)

if __name__ == "__main__":
    run_monitor()
