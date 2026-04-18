import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

# 🔑 CONFIG
BOT_TOKEN = "8657505981:AAEgs2CH8Y8yU76r_FrOKECejeJfvzR55Ug"
CHAT_ID = "-1003601267688"
ADMIN_IDS = [804349433]  # your Telegram user ID

last_update_id = None

BOLT_THREAD_ID = 10
GLOVO_THREAD_ID = 12
WOLT_THREAD_ID = 6

# 🔽 MESAJE (editabile ușor)

BOLT_MESSAGE_1 = """

🔄 <b>În seara asta la ora <b>23:59</b> se dă reset la balanța cash de pe Bolt, după care începe o nouă săptămână fiscală. 📈</b> 💱️

⚠️ Orice sumă <b>NU</b> e acoperită până în ora 23:59 <i>(miez de noapte către ziua de luni)</i> se va trage din următorul raport (<u><b>bani impozitabili</b></u>) - 👎

📌 Așadar, asigurați-vă că aveți balanța numerar pe 0 înainte de resetare, ca să nu existe probleme și confuzii. 👌✌️

📊 Țineți minte că, la Bolt, ar trebui să aveți balanța pe 0 la finalul zilei de duminică, săptămână de săptămână!

✅ Puteți face depunerea direct din aplicația Bolt Courier (actualizare în mai puțin de o oră). Dacă întâmpinați dificultăți cu depunerea, contactați asistența din aplicație -/- scrieți pe grupul Bolt/Suport General -/- cereți ajutorul unui helper.

🤝 Mulțumim de colaborare și un final de săptămână liniștit! 🙏🤍"""

BOLT_MESSAGE_2 = """🚛 <b>BOLT – Reminder FINAL</b> ⏰

⚠️ <b>Atenție!</b>
Resetarea balanței cash la Bolt are loc la ora <b>23:59</b>, după care începe o nouă săptămână fiscală.

❗ Dacă mai aveți sume nedepuse:
➡️ vor fi trase din următorul raport  
➡️ <u><b>bani impozitabili</b></u> ❌

📌 <b>Asigurați-vă că:</b>
• ați depus suma <b>integrală</b> până în ora <b>23:59</b> •
• balanța este <b>0</b> •

⛔ Nu lăsați pe ultima secundă!

🤝 Mulțumim pentru colaborare și înțelegere!"""

GLOVO_MESSAGE_1 = """

🔄 <b>În seara asta la ora 23:59 se dă reset la balanța cash de pe Glovo, după care începe o nouă săptămână fiscală. 📈</b> 💱️

⚠️ Orice sumă <b>NU</b> e acoperită până în ora <b>23:59</b> <i>(miez de noapte către ziua de luni)</i> se va trage din următorul raport (<u><b>bani impozitabili</b></u>) - 👎

📌 Așadar, asigurați-vă că aveți balanța numerar pe 0 înainte de resetare, ca să nu existe probleme și confuzii. 👌✌️

📊 Nu uitați că la Glovo, resetarea poate fi decalată până în ora 14:00 din ziua de Luni (ține de platformă, nu de noi) - de aceea recomandăm să mențineți balanța sub pragul de <b>200</b>(pe minus) în acel interval pentru a nu vi se trage din raportul care urmează, și ulterior din plata pe acea săptămână.

✅ Puteți face depunerea direct prin <a href="https://www.selfpay.ro/localizare/">SelfPay</a> (actualizare instantă). Dacă întâmpinați dificultăți cu depunerea, contactați asistența din aplicație -/- scrieți pe grupul Glovo sau Suport General -/- cereți ajutorul unui helper.

🤝 Mulțumim de colaborare și un final de săptămână liniștit! 🙏🤍"""

GLOVO_MESSAGE_2 = """🍔 <b>GLOVO – Reminder FINAL</b> ⏰

⚠️ <b>Atenție!</b>
Resetarea balanței cash la Glovo are loc la ora <b>23:59</b>, după care începe o nouă săptămână fiscală.

❗ Dacă mai aveți sume nedepuse:
➡️ vor fi trase din următorul raport  
➡️ <u><b>bani impozitabili</b></u> ❌

📌 <b>Asigurați-vă că:</b>
• ați depus suma <b>integrală</b> până în ora <b>23:59</b>
• balanța este <b>0</b>

📊 Nu uitați că la Glovo, resetarea poate fi decalată până în ora 14:00 din ziua de Luni (ține de platformă, nu de noi) - de aceea recomandăm să mențineți balanța sub pragul de 200 în acel interval pentru a nu vi se trage din raportul care urmează, și ulterior din plata pe acea săptămână.

🤝 Mulțumim pentru colaborare și înțelegere - să aveți o încheiere de săptămână liniștită și la zi cu toate! 😌🙏"""

WOLT_MESSAGE_1 = """

🔄 <b>În seara asta la ora <b>23:59</b> se dă reset la balanța cash de pe Wolt, după care începe o nouă săptămână fiscală. 📈</b> 💱

⚠️ Orice sumă <b>NU</b> e acoperită până în ora <b>23:59</b> <i>(miez de noapte către ziua de luni)</i> se va trage din următorul raport (<u><b>bani impozitabili</b></u>) - 👎

📌 Așadar, asigurați-vă că aveți balanța numerar pe 0 înainte de resetare, ca să nu existe probleme și confuzii. 👌✌️

✅ Puteți face depunerea direct prin <a href="https://youtube.com/shorts/p_dF5jPabLc?feature=share">Aircash</a> (actualizare instantă). Dacă întâmpinați dificultăți cu depunerea, contactați asistența din aplicație -/- scrieți pe grupul Wolt sau Suport General -/- cereți ajutorul unui helper.

📅 Țineți minte calendarul la Wolt pe care se calculează fiecare săptămână a lunii: <b>01–07 | 08–15 | 16–22 | 23–01</b>. Zilele în care se dă reset sunt: <b>01, 07, 15, 22</b>, în fiecare lună, la final de zi <b>(23:59)</b>.

🤝 Mulțumim de colaborare și un final de săptămână liniștit! 🙏🤍"""

WOLT_MESSAGE_2 = """

⚠️ <b>Atenție!</b>
Resetarea balanței cash la Wolt are loc la ora <b>23:59</b>, după care începe o nouă săptămână fiscală.

❗ Dacă mai aveți sume nedepuse:
➡️ vor fi trase din următorul raport  
➡️ <u><b>bani impozitabili</b></u> ❌

📌 <b>Asigurați-vă că:</b>
• ați depus suma <b>integrală</b> până în ora <b>23:59</b>
• balanța este <b>0</b>

⛔ Nu lăsați pe ultima secundă!

🤝 Mulțumim pentru colaborare și înțelegere!"""

# 🤫 Send message (auto-delete after 3 sec)
def send_message(text, thread_id=None, auto_delete=True):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
    "chat_id": CHAT_ID,
    "text": text,
    "parse_mode": "HTML",
    "disable_web_page_preview": True
}

    if thread_id:
        data["message_thread_id"] = thread_id

    response = requests.post(url, data=data).json()

    # 🧹 Auto-delete bot message
    if auto_delete and "result" in response:
        msg_id = response["result"]["message_id"]

        time.sleep(3)

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
            data={
                "chat_id": CHAT_ID,
                "message_id": msg_id
            }
        )

# ⏰ Scheduler
scheduler = BackgroundScheduler()

from datetime import timedelta

# 🧪 TEST Bolt message in 1 second
#test_time = datetime.now() + timedelta(seconds=1)

#scheduler.add_job(
#    send_message,
#    run_date=test_time,
#    args=[BOLT_MESSAGE_2, BOLT_THREAD_ID, False]
#)

# 🚛 BOLT — Duminica 12:00
scheduler.add_job(
    send_message,
    'cron',
    day_of_week='sun',
    hour=12,
    minute=0,
    args=[BOLT_MESSAGE_1, BOLT_THREAD_ID, False]
)

# 🚛 BOLT — Duminica 22:00
scheduler.add_job(
    send_message,
    'cron',
    day_of_week='sun',
    hour=22,
    minute=0,
    args=[BOLT_MESSAGE_2, BOLT_THREAD_ID, False]
)

# 🍔 GLOVO — Duminică 12:00
scheduler.add_job(
    send_message,
    'cron',
    day_of_week='sun',
    hour=12,
    minute=0,
    args=[GLOVO_MESSAGE_1, GLOVO_THREAD_ID, False]
)

# 🍔 GLOVO — Duminică 22:00
scheduler.add_job(
    send_message,
    'cron',
    day_of_week='sun',
    hour=22,
    minute=0,
    args=[GLOVO_MESSAGE_2, GLOVO_THREAD_ID, False]
)

# 🔵 WOLT — zilele 1,7,15,22 la 12:00
scheduler.add_job(
    send_message,
    'cron',
    day='1,7,15,22',
    hour=12,
    minute=0,
    args=[WOLT_MESSAGE_1, WOLT_THREAD_ID, False]
)

# 🔵 WOLT — zilele 1,7,15,22 la 22:00
scheduler.add_job(
    send_message,
    'cron',
    day='1,7,15,22',
    hour=22,
    minute=0,
    args=[WOLT_MESSAGE_2, WOLT_THREAD_ID, False]
)

# 📅 Schedule function
def schedule_custom(date_str, text, thread_id=None):
    try:
        try:
            run_date = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
        except:
            run_date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")

        scheduler.add_job(
            send_message,
            'date',
            run_date=run_date,
            args=[text, thread_id]
        )

        send_message(
            f"📅 Reminder set\n🕒 {date_str}\n📌 {text}",
            thread_id,
            auto_delete=False
        )

    except:
        send_message(
            "⚠️ Format: 16-04-2026 05:00 mesaj",
            thread_id,
            auto_delete=True
        )

# 📩 Handle Telegram messages
def handle_updates():
    global last_update_id

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": last_update_id + 1} if last_update_id else {}

    response = requests.get(url, params=params).json()

    for update in response.get("result", []):
        last_update_id = update["update_id"]

        message = update.get("message", {})
        text = message.get("text", "")

        message_id = message.get("message_id")
        user_id = message.get("from", {}).get("id")

        thread_id = message.get("message_thread_id")

        # 🚀 COMMAND: /schedule
        if text.startswith("/schedule"):

            # 🔐 Only admins allowed
            if user_id not in ADMIN_IDS:
                return

            parts = text.split(" ", 3)

            if len(parts) < 4:
                send_message(
                    "⚠️ Format: 16-04-2026 05:00 mesaj",
                    thread_id,
                    auto_delete=(user_id not in ADMIN_IDS)
                )
                return

            # 🧹 Delete admin command
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                data={
                    "chat_id": CHAT_ID,
                    "message_id": message_id
                }
            )

            date_part = parts[1]
            time_part = parts[2]
            msg_part = parts[3]

            schedule_custom(f"{date_part} {time_part}", msg_part, thread_id)

# ▶️ Start everything
scheduler.start()

print("Bot is running...")

import http.server
import socketserver
import threading

def keep_alive():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

while True:
    handle_updates()
    time.sleep(2)
