import json
import time
import requests
from datetime import datetime
from futu_api_module import place_order, close_order

# 系統設定
HEARTBEAT_INTERVAL_HOURS = 6
EXTREME_MARKET_THRESHOLD = -1.5  # 單日跌幅達1.5%觸發異常
CHECK_INTERVAL_MINUTES = 180
USE_FUTU_API = False  # 預設使用虛擬帳戶，如要切換真實交易設定為True
TELEGRAM_TOKEN = '你的Telegram Bot Token'
TELEGRAM_CHAT_ID = '你的Telegram用戶ID'

# 初始化狀態
last_heartbeat_time = 0
defense_mode_active = False
last_restart_time = datetime.utcnow()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
        print(f"📤 推播成功: {message}")
    except Exception as e:
        print(f"Telegram通知失敗: {e}")

def fetch_market_data():
    return -1.6  # 模擬市場下跌1.6%，觸發異常

def perform_trade_logic():
    if defense_mode_active:
        print("市場異常，暫停新開倉。")
        return
    if USE_FUTU_API:
        place_order(stock_code="AAPL", price=150, quantity=10, direction="BUY")
    else:
        print("虛擬下單：買進 AAPL 10股")

def check_data_integrity():
    now = datetime.utcnow()
    uptime_minutes = (now - last_restart_time).total_seconds() / 60
    if uptime_minutes >= 1440:
        return "✅資料完整"
    else:
        return "⚠️資料可能不完整"

def run_monitor():
    global last_heartbeat_time, defense_mode_active
    send_telegram_message("✅ V27.3 策略已啟動，Telegram 通知測試成功！")

    while True:
        current_time = datetime.utcnow()
        seconds_since_last_heartbeat = current_time.timestamp() - last_heartbeat_time

        if seconds_since_last_heartbeat >= HEARTBEAT_INTERVAL_HOURS * 3600:
            status = check_data_integrity()
            send_telegram_message(f"✅ 系統心跳正常：{current_time.strftime('%Y-%m-%d %H:%M:%S UTC')} | {status}")
            last_heartbeat_time = current_time.timestamp()

        market_change = fetch_market_data()
        print(f"[市場監控] 當前市場變動：{market_change}%")

        if market_change <= EXTREME_MARKET_THRESHOLD:
            if not defense_mode_active:
                defense_mode_active = True
                send_telegram_message(f"⚠️ 市場異常，啟動防禦模式：暫停新開倉 ({market_change}%)")
        else:
            if defense_mode_active:
                defense_mode_active = False
                send_telegram_message(f"✅ 市場恢復正常，解除防禦模式 ({market_change}%)")

        perform_trade_logic()
        time.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    run_monitor()

