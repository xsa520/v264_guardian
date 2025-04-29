import time
import datetime
import json
import os
import requests
import subprocess

# 從 Render 的環境變數中讀取敏感資訊
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "xsa520/v264_guardian"  # << 已正確設定你的 GitHub 倉庫

STATUS_FILE = "account_status.json"

# 預設初始帳戶狀態
account_status = {
    "total_assets": 10000,
    "total_trades": 0,
    "successful_trades": 0,
    "total_profit": 0
}

# 載入上次保存的帳戶狀態
def load_account_status():
    global account_status
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            account_status = json.load(f)
        print("✅ 成功載入上次紀錄")
    else:
        print("⚠️ 沒有找到舊資料，從初始設定開始")

# 儲存目前帳戶狀態
def save_account_status():
    with open(STATUS_FILE, "w") as f:
        json.dump(account_status, f)

# 傳送 Telegram 訊息
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"發送訊息失敗: {e}")

# 使用 git push 備份資料到 GitHub
def git_backup(filename):
    try:
        subprocess.run(["git", "add", filename], check=True)
        today = datetime.date.today().isoformat()
        commit_message = f"Auto Weekly Backup: {today}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run([
            "git", "push",
            f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
        ], check=True)
        print(f"✅ 成功推送備份檔：{filename}")
    except Exception as e:
        print(f"❌ Git 備份失敗：{e}")

# 主監控邏輯
def monitor():
    global account_status
    load_account_status()

    while True:
        now = datetime.datetime.utcnow()

        # 每天一次健康檢查（遇異常才推播）
        try:
            response = requests.get("https://google.com", timeout=10)
            if response.status_code != 200:
                send_message(f"⚠️【警報】API異常！狀態碼：{response.status_code}")
        except Exception as e:
            send_message(f"❗【緊急警報】無法連線至目標服務：{e}")

        # 每週一 UTC 0:00 推播資產報告與備份
        if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
            report = (
                f"📊【本週資產報告】\n"
                f"總資產：{account_status['total_assets']} 美元\n"
                f"交易次數：{account_status['total_trades']} 次\n"
                f"累計利潤：{account_status['total_profit']} 美元"
            )
            send_message(report)

            # 自動生成備份檔名
            monday = (datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()))
            filename = f"V26_backup_{monday}.json"
            with open(filename, "w") as f:
                json.dump(account_status, f)

            git_backup(filename)
            time.sleep(60)  # 防止重複推播/備份

        save_account_status()
        time.sleep(86400)  # 每天執行一次

if __name__ == "__main__":
    monitor()
