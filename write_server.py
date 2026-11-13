content = open('server.py', 'w', encoding='utf-8')
content.write("""import os
import time
import json
import threading
import httpx
import xml.etree.ElementTree as ET
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
    http_client = httpx.Client(follow_redirects=True)
else:
    http_client = httpx.Client(verify=False, follow_redirects=True)

client = Groq(api_key=API_KEY, http_client=http_client)
app = FastAPI()

USERS_FILE = "users_data.json"

def users_yuklash():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def users_saqlash(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def foydalanuvchi_olish(session_id):
    users = users_yuklash()
    if session_id not in users:
        users[session_id] = {"ism": "", "til": "uz", "suhbat": [], "qiziqishlar": []}
        users_saqlash(users)
    return users[session_id]

def foydalanuvchi_yangilash(session_id, data):
    users = users_yuklash()
    users[session_id] = data
    users_saqlash(users)

def yangiliklar_olish(mavzu="world"):
    manbalar = {
        "world": "https://feeds.bbci.co.uk/news/rss.xml",
        "tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "sport": "https://feeds.bbci.co.uk/news/sport/rss.xml",
        "science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    }
    url = manbalar.get(mavzu, manbalar["world"])
    try:
        r = http_client.get(url, timeout=10)
        root = ET.fromstring(r.text)
        yangiliklar = []
        for item in root.findall(".//item")[:5]:
            title = item.find("title")
            if title is not None:
                yangiliklar.append(title.text)
        return yangiliklar
    except Exception as e:
        print("Yangiliklar xatosi:", e)
        return []

def kerak_mi_yangilik(savol):
    kalit_sozlar = ["yangilik", "xabar", "news", "so'nggi", "bugun nima", "dunyo", "texnologiya", "sport", "iqtisod"]
    savol_lower = savol.lower()
    for soz in kalit_sozlar:
        if soz in savol_lower:
            return True
    return False

def yangilik_mavzusi(savol):
    savol_lower = savol.lower()
    if any(w in savol_lower for w in ["texnologiya", "tech", "it", "kompyuter"]):
        return "tech"
    if any(w in savol_lower for w in ["sport", "futbol", "basketbol"]):
        return "sport"
    if any(w in savol_lower for w in ["ilm", "fan", "science"]):
        return "science"
    if any(w in savol_lower for w in ["iqtisod", "biznes", "business", "pul"]):
        return "business"
    return "world"

bot_boshlandi = False

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
    global bot_boshlandi
    if bot_boshlandi:
        return
    bot_boshlandi = True
    print("Telegram bot ishga tushdi!")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        r = http_client.get(url, params={"timeout": 1}, timeout=5)
        updates = r.json().get("result", [])
        offset = updates[-1]["update_id"] + 1 if updates else None
    except Exception:
        offset = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {"timeout": 10, "limit": 10}
            if offset:
                params["offset"] = offset
            r = http_client.get(url, params=params, timeout=15)
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                matn = message.get("text", "")
                if chat_id and matn:
                    session_id = f"telegram_{chat_id}"
                    if matn == "/start":
                        telegram_yuborish(chat_id, "Salom! Men RAV AI!\\nIsmingizni ayting!\
\\n/yangiliklar - so'nggi xabarlar")
                    elif matn == "/yangiliklar":
                        yangiliklar = yangiliklar_olish("world")
                        if yangiliklar:
                            javob = "📰 So'nggi yangiliklar:\\n\\n" + "\\n".join([f"{i+1}. {y}" for i, y in enumerate(yangiliklar)])
                        else:
                            javob = "Yangiliklar yuklanmadi."
                        telegram_yuborish(chat_id, javob)
                    else:
                        javob = gemini_javob(matn, session_id)
                        telegram_yuborish(chat_id, javob)
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
        "angliya": "London", "england": "London",
        "germaniya": "Berlin", "germany": "Berlin",
        "xitoy": "Beijing", "china": "Beijing",
        "yaponiya": "Tokyo", "japan": "Tokyo",
        "amerika": "New+York", "usa": "New+York",
        "hindiston": "Delhi", "india": "Delhi",
        "italiya": "Rome", "italy": "Rome",
        "turkiya": "Istanbul", "turkey": "Istanbul",
        "ozbekiston": "Tashkent", "uzbekistan": "Tashkent",
        "qozogiston": "Almaty", "kazakhstan": "Almaty",
        "misr": "Cairo", "egypt": "Cairo",
        "braziliya": "Sao+Paulo", "brazil": "Sao+Paulo",
        "avstraliya": "Sydney", "australia": "Sydney",
        "kanada": "Toronto", "canada": "Toronto",
        "pokiston": "Karachi", "pakistan": "Karachi",
        "tailand": "Bangkok", "thailand": "Bangkok",
        "saudiya": "Riyadh", "saudi": "Riyadh",
        "bae": "Dubai", "uae": "Dubai",
        "ispaniya": "Madrid", "spain": "Madrid",
        "ukraina": "Kyiv", "ukraine": "Kyiv",
        "ozarbayjon": "Baku", "azerbaijan": "Baku",
        "qirgiziston": "Bishkek", "kyrgyzstan": "Bishkek",
        "tojikiston": "Dushanbe", "tajikistan": "Dushanbe",
        "turkmaniston": "Ashgabat", "turkmenistan": "Ashgabat",
        "afgoniston": "Kabul", "afghanistan": "Kabul",
        "marokash": "Casablanca", "morocco": "Casablanca",
        "keniya": "Nairobi", "kenya": "Nairobi",
        "kolumbiya": "Bogota", "colombia": "Bogota",
        "peru": "Lima", "chili": "Santiago", "chile": "Santiago",
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
    natija = ""
    if kerak_mi_yangilik(savol):
        mavzu = yangilik_mavzusi(savol)
        yangiliklar = yangiliklar_olish(mavzu)
        if yangiliklar:
           natija += "Yangiliklar:\
" + "\\n".join([f"{i+1}. {y[:80]}" for i, y in enumerate(yangiliklar[:3])]) + "\
"

    kalit_sozlar = ["hozir", "bugun", "ob-havo", "ob havo", "weather", "harorat", "iqlim"]
    if any(soz in savol.lower() for soz in kalit_sozlar):
        try:
            shahar = shahar_topish(savol)
            url = "https://wttr.in/" + shahar + "?format=3"
            r = http_client.get(url, timeout=5)
            if r.status_code == 200:
                natija += "Ob-havo: " + r.text
        except Exception as e:
            print("Ob-havo xatosi:", e)
    return natija

def gemini_javob(savol, session_id="default"):
    user = foydalanuvchi_olish(session_id)
    internet_malumot = internet_qidirish(savol)
    user["suhbat"].append({"role": "user", "content": savol})
    if len(user["suhbat"]) > 20:
        user["suhbat"] = user["suhbat"][-20:]
    system = "Sen RAV AI degan eng aqlli shaxsiy assistantsan. Foydalanuvchi qaysi tilda yozsa, osha tilda javob ber. Suhbat tarixini eslab qol. Foydalanuvchi ismini aytsa eslab qol."
    if user["ism"]:
        system += f" Foydalanuvchi ismi: {user['ism']}."
    if internet_malumot:
        system += "\\n\
Internet malumotlari:\\n" + internet_malumot
    messages = [{"role": "system", "content": system}] + user["suhbat"]
    for urinish in range(3):
        try:
            response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=messages,
                max_tokens=2048,
            )
            javob = response.choices[0].message.content
            user["suhbat"].append({"role": "assistant", "content": javob})
            if not user["ism"] and "ismim" in savol.lower():
                words = savol.split()
                for i, w in enumerate(words):
                    if w.lower() in ["ismim", "ismim:"]:
                        if i + 1 < len(words):
                            user["ism"] = words[i + 1].strip(".,!")
            foydalanuvchi_yangilash(session_id, user)
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
    session_id: str = "default"

class RasmModel(BaseModel):
    matn: str

@app.get("/", response_class=HTMLResponse)
def bosh_sahifa():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/savol")
def savol_yuborish(data: SavolModel):
    javob = gemini_javob(data.matn, data.session_id)
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
""")
content.close()
print("Tayyor!")