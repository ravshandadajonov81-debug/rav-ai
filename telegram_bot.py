import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "9010906740:AAFruhdfoKLCbVr4d_d1iSVCnoXeTKPS6Ao")
RAV_AI_URL = "http://127.0.0.1:8000/savol"

http = httpx.Client(verify=False)

def telegram_yuborish(chat_id, matn):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    http.post(url, json={"chat_id": chat_id, "text": matn, "parse_mode": "Markdown"})

def javob_olish(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    r = http.get(url, params=params, timeout=35)
    return r.json()

def rav_ai_javob(matn):
    try:
        r = http.post(RAV_AI_URL, json={"matn": matn}, timeout=30)
        return r.json().get("javob", "Xato yuz berdi!")
    except Exception:
        return "Server bilan aloqa yo'q!"

print("RAV AI Telegram bot ishga tushdi! @ravai_official_bot")

offset = None
while True:
    try:
        yangiliklar = javob_olish(offset)
        for update in yangiliklar.get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            matn = message.get("text", "")
            if chat_id and matn:
                print(f"Xabar: {matn}")
                if matn == "/start":
                    telegram_yuborish(chat_id, "Salom! Men *RAV AI* — aqlli yordamchingizman! 🤖\nHar qanday savolingizni yozing!")

                else:
                    javob = rav_ai_javob(matn)
                    telegram_yuborish(chat_id, javob)
    except Exception as e:
        print("Xato:", e)
        time.sleep(5)