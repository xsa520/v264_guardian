import time
import datetime
import json
import os
import requests
import subprocess

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "xsa520/v264_guardian"
HEARTBEAT_MODE = os.getenv("HEARTBEAT_MODE", "OFF")  # 預設不開

STATUS_FILE = "account_status.json"
account_status = {
    "total_assets": 10000,
    "total_trades": 0,
    "successful_trades": 0,
    "total_profit": 0
}

last_heartbeat_hour = -1  # 記錄上次發送的時段

def load_account_status():
    global account_status
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            account_status = json.load(f)
        print("✅ 成功載入上次紀錄")
    else:
        print("⚠️ 沒有找到舊資料，從初始設定開始")

def save_account_status():
    with open(STATUS_FILE, "w") as f:
        json.dump(account_status, f)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"發送訊息失敗: {e}")

def git_backup(filename):
    try:
        subprocess.run(["git", "add", filename], check=True)
        today = datetime.date.today().isoformat()
        commit_message = f"Auto Backup: {today}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run([
            "git", "push",
            f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
        ], check=True)
        print(f"✅ 成功推送備份檔案：{filename}")
    except Exception as e:
        print(f"❌ Git 備份失敗：{e}")

def generate_backup_filename(prefix):
    today = datetime.date.today()
    return f"{prefix}_{today}.json"

def generate_month_backup():
    today = datetime.date.today()
    if today.day == 1:
        last_month = today.replace(day=1) - datetime.timedelta(days=1)
        filename = f"Month_Report_{last_month.strftime('%Y-%m')}.json"
        with open(filename, "w") as f:
            json.dump(account_status, f)
        git_backup(filename)

def generate_quarter_backup():
    today = datetime.date.today()
    if today.month in [1, 4, 7, 10] and today.day == 1:
        last_quarter_month = today.month - 1
        quarter = (last_quarter_month // 3) + 1
        filename = f"Quarter_Report_{today.year}-Q{quarter}.json"
        with open(filename, "w") as f:
            json.dump(account_status, f)
        git_backup(filename)

def generate_year_backup():
    today = datetime.date.today()
    if today.month == 1 and today.day == 1:
        last_year = today.year - 1
        filename = f"Annual_Report_{last_year}.json"
        with open(filename, "w") as f:
            json.dump(account_status, f)
        git_backup(filename)

def heartbeat_check(now):
    global last_heartbeat_hour
    if HEARTBEAT_MODE.upper() != "ON":
        return
    if now.hour % 6 == 0 and now.hour != last_heartbeat_hour:
        text = (
            f"✅【系統心跳回報】\n"
            f"時間：{now.strftime('%Y-%m-%d %H:%M')} UTC\n"
            f"目前總資產：{account_status['total_assets']} 美元"
        )
        send_message(text)
        last_heartbeat_hour = now.hour

def monitor():
    global account_status
    load_account_status()

    while True:
        now = datetime.datetime.utcnow()

        # 健康巡檢
        try:
            response = requests.get("https://google.com", timeout=10)
            if response.status_code != 200:
                send_message(f"⚠️【警報】API異常！狀態碼：{response.status_code}")
        except Exception as e:
            send_message(f"❗【緊急警報】無法連線至目標服務：{e}")

        # 每週一報告
        if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
            report = (
                f"📊【本週資產報告】\n"
                f"總資產：{account_status['total_assets']} 美元\n"
                f"交易次數：{account_status['total_trades']} 次\n"
                f"累計利潤：{account_status['total_profit']} 美元"
            )
            send_message(report)

            monday = (datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()))
            filename = f"V26_backup_{monday}.json"
            with open(filename, "w") as f:
                json.dump(account_status, f)
            git_backup(filename)
            time.sleep(60)

        # 心跳
        heartbeat_check(now)

        # 備份：月報、季報、年報
        generate_month_backup()
        generate_quarter_backup()
        generate_year_backup()

        save_account_status()
        time.sleep(86400)  # 每日一次

if __name__ == "__main__":
    monitor()
