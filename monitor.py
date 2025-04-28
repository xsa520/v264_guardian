import time
import requests

BOT_TOKEN = "7916180466:AAF4lT4JPOKkfkm1LvIiA0NfTWaiSmT0Byo"
CHAT_ID = "7398446407"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def monitor():
    while True:
        print("巡邏中...")
        time.sleep(180)  # 每3分鐘掃描一次

if __name__ == "__main__":
    send_message("【V26.4軍監系統啟動】巡邏中，每3分鐘掃描一次！")
    monitor()
