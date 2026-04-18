import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

# 🔑 CONFIG (IMPORTANT — pune valorile tale reale)
BOT_TOKEN = "8657505981:AAEgs2CH8Y8yU76r_FrOKECejeJfvzR55Ug"
CHAT_ID = "-1003601267688"
THREAD_ID = 10  # topic Bolt (poți schimba dacă vrei)

# 🔧 send message simplu
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    # dacă vrei să trimită în topic
    if THREAD_ID:
        data["message_thread_id"] = THREAD_ID

    requests.post(url, data=data, timeout=10)


# ⏰ scheduler
scheduler = BackgroundScheduler()

# 🧪 TEST — trimite în 3 secunde
run_time = datetime.now() + timedelta(seconds=3)

scheduler.add_job(
    send_message,
    'date',
    run_date=run_time,
    args=["🧪 TEST: Dacă vezi mesajul ăsta, botul funcționează PERFECT!"]
)

scheduler.start()

print("Test bot running...")

# 🔁 keep alive loop
while True:
    time.sleep(1)
