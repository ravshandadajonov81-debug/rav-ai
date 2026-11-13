import os
import time
import threading
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "9010906740:AAFruhdfoKLCbVr4d_d1iSVCnoXeTKPS6Ao")
IS_RENDER = os.environ.get("RENDER", False)

if IS_RENDER:
    http_client = httpx.Client()
else:
    http_client = httpx.Client(verify=False)

client = Groq(api_key=API_KEY, http_client=http_client)
app = FastAPI()

suhbat_tarixi = []
telegram_suhbatlar = {}

def keep_alive():
    while True:
        time.sleep(600)
        try:
            http_client.get("https://rav-ai.onrender.com", timeout=10)
            print("Keep alive!")
        except Exception:
            pass

def telegram_yuborish(chat_id, matn):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        http_client.post(url, json={"chat_id": chat_id, "text": matn})
    except Exception as e:
        print("Telegram xato:", e)

def telegram_bot():
    offset = None
    print("Telegram bot ishga tushdi!")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
            r = http_client.get(url, params=params, timeout=35)
            yangiliklar = r.json()
            for update in yangiliklar.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                matn = message.get("text", "")
                if chat_id and matn:
                    if matn == "/start":
                        telegram_yuborish(chat_id, "Salom! Men RAV AI — aqlli yordamchingizman! Har qanday savolingizni yozing!")
                    else:
                        if chat_id not in telegram_suhbatlar:
                            telegram_suhbatlar[chat_id] = []
                        telegram_suhbatlar[chat_id].append({"role": "user", "content": matn})
                        if len(telegram_suhbatlar[chat_id]) > 20:
                            telegram_suhbatlar[chat_id] = telegram_suhbatlar[chat_id][-20:]
                        messages = [{"role": "system", "content": "Sen RAV AI degan eng aqlli assistantsan. Foydalanuvchi qaysi tilda yozsa, osha tilda javob ber. Ismini eslab qol."}] + telegram_suhbatlar[chat_id]
                        try:
                            response = client.chat.completions.create(
                                model="openai/gpt-oss-120b",
                                messages=messages,
                                max_tokens=1024,
                            )
                            javob = response.choices[0].message.content
                            telegram_suhbatlar[chat_id].append({"role": "assistant", "content": javob})
                            telegram_yuborish(chat_id, javob)
                        except Exception:
                            telegram_yuborish(chat_id, "Hozir band. Qayta urinib koring!")
        except Exception as e:
            print("Bot xato:", e)
            time.sleep(5)

threading.Thread(target=keep_alive, daemon=True).start()
threading.Thread(target=telegram_bot, daemon=True).start()

def shahar_topish(savol):
    savol_lower = savol.lower()
    mamlakatlar = {
        "fransiya": "Paris", "france": "Paris",
        "rossiya": "Moscow", "russia": "Moscow",
        "angliya": "London", "england": "London", "uk": "London",
        "germaniya": "Berlin", "germany": "Berlin",
        "xitoy": "Beijing", "china": "Beijing",
        "yaponiya": "Tokyo", "japan": "Tokyo",
        "amerika": "New+York", "usa": "New+York",
        "koreys": "Seoul", "korea": "Seoul",
        "hindiston": "Delhi", "india": "Delhi",
        "italiya": "Rome", "italy": "Rome",
        "turkiya": "Istanbul", "turkey": "Istanbul",
        "ozbekiston": "Tashkent", "uzbekistan": "Tashkent",
        "qozogiston": "Almaty", "kazakhstan": "Almaty",
        "misr": "Cairo", "egypt": "Cairo",
        "braziliya": "Sao+Paulo", "brazil": "Sao+Paulo",
        "avstraliya": "Sydney", "australia": "Sydney",
        "kanada": "Toronto", "canada": "Toronto",
        "meksika": "Mexico+City", "mexico": "Mexico+City",
        "argentina": "Buenos+Aires",
        "pokiston": "Karachi", "pakistan": "Karachi",
        "tailand": "Bangkok", "thailand": "Bangkok",
        "indoneziya": "Jakarta", "indonesia": "Jakarta",
        "malayziya": "Kuala+Lumpur", "malaysia": "Kuala+Lumpur",
        "saudiya": "Riyadh", "saudi": "Riyadh",
        "qatar": "Doha", "doha": "Doha",
        "bae": "Dubai", "uae": "Dubai",
        "ispaniya": "Madrid", "spain": "Madrid",
        "niderlandiya": "Amsterdam", "netherlands": "Amsterdam",
        "ukraina": "Kyiv", "ukraine": "Kyiv",
        "ozarbayjon": "Baku", "azerbaijan": "Baku",
        "qirgiziston": "Bishkek", "kyrgyzstan": "Bishkek",
        "tojikiston": "Dushanbe", "tajikistan": "Dushanbe",
        "turkmaniston": "Ashgabat", "turkmenistan": "Ashgabat",
        "afgoniston": "Kabul", "afghanistan": "Kabul",
        "singapur": "Singapore", "singapore": "Singapore",
        "marokash": "Casablanca", "morocco": "Casablanca",
        "keniya": "Nairobi", "kenya": "Nairobi",
        "kolumbiya": "Bogota", "colombia": "Bogota",
        "peru": "Lima", "chili": "Santiago", "chile": "Santiago",
        "kuba": "Havana", "cuba": "Havana",
    }
    for kalit, shahar in mamlakatlar.items():
        if kalit in savol_lower:
            return shahar
    shaharlar = [
        "toshkent", "samarqand", "buxoro", "namangan", "andijon",
        "dubai", "dubay", "moscow", "london", "paris", "berlin",
        "rome", "madrid", "amsterdam", "vienna", "new york",
        "beijing", "shanghai", "tokyo", "seoul", "delhi", "mumbai",
        "istanbul", "cairo", "sydney", "singapore", "bangkok",
        "karachi", "tehran", "kyiv", "baku", "bishkek",
        "dushanbe", "ashgabat", "almaty", "riyadh", "doha",
    ]
    for shahar in shaharlar:
        if shahar in savol_lower:
            return shahar.replace(" ", "+").title()
    return "Tashkent"

def internet_qidirish(savol):
    try:
        shahar = shahar_topish(savol)
        url = "https://wttr.in/" + shahar + "?format=3"
        r = http_client.get(url, timeout=5)
        if r.status_code == 200:
            return "Ob-havo: " + r.text
    except Exception as e:
        print("Ob-havo xatosi:", e)
    return ""

def kerak_mi_internet(savol):
    kalit_sozlar = ["hozir", "bugun", "ob-havo", "ob havo", "weather", "harorat", "iqlim"]
    savol_lower = savol.lower()
    for soz in kalit_sozlar:
        if soz in savol_lower:
            return True
    return False

def gemini_javob(savol):
    global suhbat_tarixi
    internet_malumot = ""
    if kerak_mi_internet(savol):
        internet_malumot = internet_qidirish(savol)
    suhbat_tarixi.append({"role": "user", "content": savol})
    if len(suhbat_tarixi) > 20:
        suhbat_tarixi = suhbat_tarixi[-20:]
    system = "Sen RAV AI degan eng aqlli shaxsiy assistantsan. Foydalanuvchi qaysi tilda yozsa, osha tilda javob ber. Suhbat tarixini eslab qol. Foydalanuvchi ismini aytsa eslab qol."
    if internet_malumot:
        system += "\nInternet malumotlari:\n" + internet_malumot
    messages = [{"role": "system", "content": system}] + suhbat_tarixi
    for urinish in range(3):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                max_tokens=1024,
            )
            javob = response.choices[0].message.content
            suhbat_tarixi.append({"role": "assistant", "content": javob})
            return javob
        except Exception:
            if urinish < 2:
                time.sleep(2)
            else:
                return "Hozir server band. Biroz kutib qayta yuboring!"

def rasm_prompt_tayyorla(matn):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": f"Convert this to a detailed English image prompt (max 15 words, no quotes): {matn}"}],
            max_tokens=40,
        )
        return response.choices[0].message.content.strip().strip('"').strip("'")
    except Exception:
        return matn

class SavolModel(BaseModel):
    matn: str

class RasmModel(BaseModel):
    matn: str

@app.get("/", response_class=HTMLResponse)
def bosh_sahifa():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/savol")
def savol_yuborish(data: SavolModel):
    javob = gemini_javob(data.matn)
    return {"javob": javob}

@app.post("/rasm")
def rasm_yaratish(data: RasmModel):
    try:
        prompt = rasm_prompt_tayyorla(data.matn)
        prompt_full = prompt + ", ultra realistic, 4K, professional photography, detailed"
        url = "https://image.pollinations.ai/prompt/" + prompt_full.replace(" ", "%20") + "?model=flux&width=1024&height=1024&nologo=true"
        return {"rasm_url": url}
    except Exception as e:
        return {"xato": str(e)}
