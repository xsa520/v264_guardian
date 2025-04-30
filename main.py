from flask import Flask
import os
import threading
import monitor  # 確保 monitor.py 已存在

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ V27.3 Guardian Strategy is Running."

if __name__ == "__main__":
    threading.Thread(target=monitor.run_monitor, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
