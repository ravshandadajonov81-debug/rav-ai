import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
import os
import time
import json
import threading
import httpx
import xml.etree.ElementTree as ET
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
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

def telegram_xabar_qayta_ishlash(update):
    try:
        message = update.get("message", {})
        chat_type = message.get("chat", {}).get("type", "private")
        bot_username = "ravo7_ai_bot"
        if chat_type in ["group", "supergroup"]:
            matn_raw = message.get("text", "")
            if ("@" + bot_username) not in matn_raw and not matn_raw.startswith("/"):
                return
            message["text"] = matn_raw.replace("@" + bot_username, "").strip()
        chat_id = message.get("chat", {}).get("id")
        matn = message.get("text", "")
        if chat_id and matn:
            matn = sleng_tozala(matn)
            message["text"] = matn
            try:
                aniq_shahar = None
                try:
                    aniq_shahar = joy_nomini_ai_topish(matn)
                except Exception:
                    aniq_shahar = None
                aniq_mavzu = "umumiy"
                matn_kichik = matn.lower()
                if any(s in matn_kichik for s in ["ob-havo", "ob havo", "havo", "weather", "harorat"]):
                    aniq_mavzu = "ob-havo"
                elif any(s in matn_kichik for s in ["valyuta", "kurs", "dollar", "som", "rubl"]):
                    aniq_mavzu = "valyuta"
                elif any(s in matn_kichik for s in ["vaqt", "soat", "time"]):
                    aniq_mavzu = "vaqt"
                aniq_ism = None
                if "ismim" in matn_kichik:
                    soz_royxati = matn.split()
                    for i2, s2 in enumerate(soz_royxati):
                        if s2.lower().startswith("ismim") and i2 + 1 < len(soz_royxati):
                            aniq_ism = soz_royxati[i2 + 1].strip(".,!")
                            break
                foydalanuvchini_saqla(chat_id, ism=aniq_ism, shahar=aniq_shahar, mavzu=aniq_mavzu)
            except Exception as mongo_xato:
                print("Mongo saqlash xatosi:", mongo_xato)
            session_id = f"telegram_{chat_id}"
            if matn == "/start":
                telegram_yuborish(chat_id, "Salom! Men RAV AI!\nIsmingizni ayting!/yangiliklar - so'nggi xabarlar")
            elif matn == "/stat":
                users = users_yuklash()
                jami_user = len(users)
                jami_xabar = sum(len(u.get("suhbat", [])) for u in users.values())
                javob_stat = "RAV AI statistikasi:" + chr(10) + chr(10) + "Jami foydalanuvchilar: " + str(jami_user) + chr(10) + "Jami xabarlar: " + str(jami_xabar)
                telegram_yuborish(chat_id, javob_stat)
            elif matn == "/yangiliklar":
                yangiliklar = yangiliklar_olish("world")
                if yangiliklar:
                    javob = "So'nggi yangiliklar:\n" + "\n".join([f"{i+1}. {y}" for i, y in enumerate(yangiliklar)])
                else:
                    javob = "Yangiliklar yuklanmadi."
                telegram_yuborish(chat_id, javob)
            else:
                javob = gemini_javob(matn, session_id)
                telegram_yuborish(chat_id, javob)
    except Exception as e:
        print("Xabar xatosi:", e)

def webhook_ornatish():
    time.sleep(3)
    try:
        webhook_url = f"https://rav-ai.onrender.com/telegram/{TELEGRAM_TOKEN}"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        r = http_client.post(url, json={"url": webhook_url})
        print("Webhook:", r.json())
    except Exception as e:
        print("Webhook xatosi:", e)

threading.Thread(target=keep_alive, daemon=True).start()
threading.Thread(target=webhook_ornatish, daemon=True).start()

def valyuta_nomlari():
    return {
        'dollar': 'USD', 'dollari': 'USD', 'dolar': 'USD', 'dólar': 'USD', 'доллар': 'USD',
        'الدولار': 'USD', 'دولار': 'USD', '달러': 'USD', '美元': 'USD', 'usd': 'USD',
        'euro': 'EUR', 'yevro': 'EUR', 'евро': 'EUR', 'اليورو': 'EUR', '유로': 'EUR', '欧元': 'EUR', 'eur': 'EUR',
        'rubl': 'RUB', 'rublo': 'RUB', 'рубль': 'RUB', 'рубл': 'RUB', 'الروبل': 'RUB', '루블': 'RUB', '卢布': 'RUB', 'rub': 'RUB',
        'funt': 'GBP', 'sterling': 'GBP', 'фунт': 'GBP', 'الجنيه': 'GBP', '파운드': 'GBP', '英镑': 'GBP',
        'yen': 'JPY', 'yena': 'JPY', 'иена': 'JPY', 'الين': 'JPY', '엔화': 'JPY', '日元': 'JPY',
        'yuan': 'CNY', 'юань': 'CNY', 'اليوان': 'CNY', '위안': 'CNY', '人民币': 'CNY',
        'lira': 'TRY', 'лира': 'TRY', 'الليرة': 'TRY', '리라': 'TRY', '里拉': 'TRY',
        'dirham': 'AED', 'дирхам': 'AED', 'الدرهم': 'AED', '디르함': 'AED', '迪拉姆': 'AED',
        'tenge': 'KZT', 'тенге': 'KZT',
        'manat': 'AZN', 'манат': 'AZN',
        'som': 'KGS',
        'hryvnia': 'UAH', 'гривна': 'UAH', 'гривня': 'UAH',
        'rupiya': 'INR', 'rupee': 'INR', 'рупия': 'INR', 'الروبية': 'INR', '루피': 'INR', '卢比': 'INR',
        'von': 'KRW', 'won': 'KRW', 'вона': 'KRW', '원화': 'KRW', '韩元': 'KRW',
        'frank': 'CHF', 'franc': 'CHF', 'франк': 'CHF', '法郎': 'CHF',
        'real': 'BRL', 'реал': 'BRL',
    }

VALYUTA_KOD_NOM = {
    "USD": "Dollar", "EUR": "Euro", "RUB": "Rubl", "GBP": "Funt sterling",
    "JPY": "Yen", "CNY": "Yuan", "TRY": "Lira", "AED": "Dirham",
    "KZT": "Tenge", "AZN": "Manat", "KGS": "Som", "UAH": "Grivna",
    "INR": "Rupiya", "KRW": "Von", "CHF": "Shveytsariya franki", "BRL": "Real",
}

def miqdor_topish(savol):
    import re
    topilgan = re.findall(r"\d[\d\s.,]*\d|\d", savol)
    for raqam_matni in topilgan:
        tozalangan = raqam_matni.replace(" ", "").replace(",", "")
        try:
            qiymat = float(tozalangan)
            if qiymat > 0:
                return qiymat
        except ValueError:
            continue
    return 1

def valyuta_kursi_olish(maqsad=None, miqdor=1):
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        r = http_client.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            rates = d.get("rates", {})
            uzs = rates.get("UZS", 0)
            if maqsad and maqsad in rates and maqsad != 'UZS':
                kurs = rates[maqsad]
                som_narx = round((uzs / kurs) * miqdor)
                nom = VALYUTA_KOD_NOM.get(maqsad, maqsad)
                miqdor_matni = str(int(miqdor)) if miqdor == int(miqdor) else str(miqdor)
                return miqdor_matni + " " + nom + " (" + maqsad + ") = " + str(som_narx) + " som"
            eur = rates.get("EUR", 0)
            rub = rates.get("RUB", 0)
            natija = "Valyuta kurslari:" + chr(10)
            natija += chr(10) + "1 Dollar = " + str(round(uzs)) + " som"
            if eur:
                natija += chr(10) + "1 Euro = " + str(round(uzs/eur)) + " som"
            if rub:
                natija += chr(10) + "1 Rubl = " + str(round(uzs/rub)) + " som"
            return natija
    except Exception as e:
        print("Valyuta xatosi:", e)
    return "Valyuta malumotini olib bolmadi"

def valyuta_kodi_topish(savol):
    savol_l = savol.lower()
    for soz, kod in VALYUTA_ISHONCHLI_SOZLAR.items():
        if soz in savol_l:
            return kod
    nomlar = valyuta_nomlari()
    for nom, kod in nomlar.items():
        if nom in VALYUTA_NOANIQ_SOZLAR and nom in savol_l:
            if any(blok in savol_l for blok in VALYUTA_NOANIQ_BLOKLOVCHI):
                continue
            return kod
        elif nom not in VALYUTA_NOANIQ_SOZLAR and nom in savol_l:
            return kod
    return None

def kerak_mi_internet_ai(savol):
    try:
        messages = [
            {"role": "system", "content": "Foydalanuvchi savoli internetdan joriy yoki real vaqt malumot (yangiliklar, musobaqa natijalari, kim yutdi/goliб boldi, bugungi voqealar, statistika, aniq ommaviy faktlar) qidirishni talab qiladimi? Faqat HA yoki YOQ deb javob ber, boshqa hech narsa yozma."},
            {"role": "user", "content": savol},
        ]
        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, max_tokens=200)
        javob = response.choices[0].message.content.strip().lower()
        if "ha" in javob[:10]:
            return True
        return False
    except Exception as e:
        print("Internet aniqlash xatosi:", e)
        return False

def kerak_mi_valyuta_ai(savol):
    try:
        messages = [
            {"role": "system", "content": "Foydalanuvchi savoli valyuta kursi, pul almashtirish narxi haqida so\'rayaptimi (masalan dollar, euro, yuan va hokazo pul birligining somga yoki boshqa pulga nisbatan narxi)? Agar bu boshqa mavzu (masport, odam ismi, joy nomi va h.k.) bolsa, YOQ deb javob ber. Faqat HA yoki YOQ deb javob ber, boshqa hech narsa yozma."},
            {"role": "user", "content": savol},
        ]
        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, max_tokens=200)
        javob = response.choices[0].message.content.strip().lower()
        if "ha" in javob[:10]:
            return True
        return False
    except Exception as e:
        print("Valyuta AI aniqlash xatosi:", e)
        return False

VALYUTA_RUXSAT_ETILGAN_KODLAR = {"USD", "EUR", "RUB", "CNY", "GBP", "JPY", "TRY", "AED", "KZT", "AZN", "KGS", "UAH", "INR", "KRW", "CHF", "BRL"}

VALYUTA_ISHONCHLI_SOZLAR = {
    "dollar": "USD", "dollari": "USD", "dolar": "USD", "doliar": "USD",
    "euro": "EUR", "yevro": "EUR",
    "rubl": "RUB", "rublo": "RUB", "rubil": "RUB", "rubl'": "RUB",
    "yuan": "CNY",
    "funt sterling": "GBP", "sterling": "GBP",
    "yen": "JPY", "yena": "JPY",
    "lira": "TRY",
    "dirham": "AED",
    "tenge": "KZT",
    "manat": "AZN",
    "hryvnia": "UAH", "grivna": "UAH",
    "rupiya": "INR",
    "shveytsariya franki": "CHF",
}

VALYUTA_NOANIQ_SOZLAR = {"real": "BRL", "frank": "CHF", "franc": "CHF", "won": "KRW", "von": "KRW"}
VALYUTA_NOANIQ_BLOKLOVCHI = [
    "madrid", "sociedad", "futbol", "football", "match", "o\'yin", "oyin", "jamoa", "sport",
    "who won", "game", "played", "player", "team", "cup", "league", "championship",
    "goldi", "g\'oldi", "qoldi",
]

def valyuta_kodi_ai_topish(savol):
    try:
        savol_l = savol.lower()
        for soz, kod in VALYUTA_ISHONCHLI_SOZLAR.items():
            if soz in savol_l:
                return kod
        for soz, kod in VALYUTA_NOANIQ_SOZLAR.items():
            if soz in savol_l:
                if any(blok in savol_l for blok in VALYUTA_NOANIQ_BLOKLOVCHI):
                    return None
                return kod
        return None
    except Exception as e:
        print("Valyuta kodi topish xatosi:", e)
        return None

def internetdan_qidirish(savol):
    from ddgs import DDGS
    backendlar = ["bing", "google", "duckduckgo"]
    for nom in backendlar:
        try:
            natijalar = DDGS(verify=False).text(savol, max_results=4, backend=nom)
            if natijalar:
                matn = ""
                for n in natijalar[:4]:
                    sarlavha = n.get("title", "").strip()
                    if len(sarlavha) > 70:
                        sarlavha = sarlavha[:70] + "..."
                    tavsif = n.get("body", "").strip()
                    if len(tavsif) > 180:
                        tavsif = tavsif[:180] + "..."
                    matn += "- " + sarlavha + ": " + tavsif + chr(10)
                return matn
        except Exception as e:
            print("Internet qidiruv xatosi (" + nom + "):", e)
    return None

VALYUTA_UMUMIY_SOZLAR = [
    "valyuta", "kurs", "exchange rate", "currency", "курс", "валюта",
    "tasso di cambio", "valuta", "taux de change", "devise",
    "wechselkurs", "wahrung", "tipo de cambio", "divisa",
    "汇率", "货币", "exchange", "kurs walut",
    "سعر الصرف", "عملة", "환율", "nilai tukar", "kurs mata uang",
]

def kerak_mi_valyuta(savol):
    savol_l = savol.lower()
    if any(s in savol_l for s in VALYUTA_UMUMIY_SOZLAR):
        return True
    for soz in VALYUTA_ISHONCHLI_SOZLAR:
        if soz in savol_l:
            return True
    for soz in VALYUTA_NOANIQ_SOZLAR:
        if soz in savol_l:
            if any(blok in savol_l for blok in VALYUTA_NOANIQ_BLOKLOVCHI):
                return False
            return True
    return False

from zoneinfo import ZoneInfo
from datetime import datetime

def kerak_mi_vaqt_ai(savol):
    for urinish in range(3):
        try:
            messages = [
                {"role": "system", "content": "Javob faqat HA yoki YOQ bilan ber. Boshqa hech narsa yozma. Foydalanuvchi matni vaqtni yoki soatni (hozir necha bolganini, biror joyda soat nechaligini) sorayaptimi?"},
                {"role": "user", "content": savol},
            ]
            response = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=200)
            javob = response.choices[0].message.content.strip().lower()
            return "ha" in javob
        except Exception:
            if urinish < 2:
                time.sleep(1)
            else:
                return False

def kerak_mi_vaqt(savol):
    kalit = ["soat necha", "vaqt qancha", "hozir soat", "time", "nechada", "soat nechada", "saat kac", "saat kac", "necha soat", "soat nech", "skolko vremeni", "what time", "сколько времени", "который час", "саат нечэ", "现在几点", "几点了", "che ore sono", "che ora", "quelle heure", "wie spat", "que hora", "que horas", "hoe laat", "ile godzina", "kolik je hodin", "pukul berapa", "jam berapa", "saat kac"]
    return any(k in savol.lower() for k in kalit)

def joy_vaqt_zonasi_topish(joy_nomi):
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        r = http_client.get(url, params={"name": joy_nomi, "count": 1}, timeout=8)
        if r.status_code == 200:
            d = r.json()
            natija = d.get("results")
            if natija:
                joy = natija[0]
                return joy.get("timezone"), joy.get("name")
    except Exception as e:
        print("Geocoding xatosi:", e)
    return None, None

def joy_nomini_ai_topish(savol):
    for urinish in range(3):
        try:
            messages = [
                {"role": "system", "content": "Sen aniq joy-nomi ajratuvchisan. Vazifang: foydalanuvchi matnida vaqt sorovi qilingan ANIQ shahar yoki davlat nomini topish. Soz hozir, soat, vaqt kabi sozlarga etibor berma, ular joy nomi emas. Faqat haqiqiy geografik joy nomini top. Javobni albatta lotin harflarida yoz, masalan Bangladesh, Istanbul, Tashkent. Agar matnda hech qanday joy nomi bolmasa, faqat NONE deb yoz. Hech qanday izoh yozma, faqat lotin harflarida joy nomi yoki NONE."},
                {"role": "user", "content": savol},
            ]
            response = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=200)
            joy = response.choices[0].message.content.strip()
            if joy.upper() == "NONE" or len(joy) < 2:
                return None
            return joy
        except Exception:
            if urinish < 2:
                time.sleep(1)
            else:
                return None

LANGUAGES = {"uz": "uz_UZ", "en": "en_US", "ru": "ru_RU", "fr": "fr_FR", "it": "it_IT", "de": "de_DE", "es": "es_ES", "tr": "tr_TR", "ar": "ar", "zh": "zh_CN", "ja": "ja_JP", "ko": "ko_KR", "pt": "pt_PT", "hi": "hi_IN", "uk": "uk_UA", "pl": "pl_PL", "nl": "nl_NL", "sv": "sv_SE", "fa": "fa_IR", "id": "id_ID", "tg": "tg_TJ", "bn": "bn_BD", "th": "th_TH", "vi": "vi_VN", "el": "el_GR", "he": "he_IL", "ro": "ro_RO", "cs": "cs_CZ", "da": "da_DK", "fi": "fi_FI", "no": "nb_NO", "hu": "hu_HU", "sr": "sr_RS", "hr": "hr_HR", "bg": "bg_BG", "sk": "sk_SK", "sl": "sl_SI", "ms": "ms_MY", "ta": "ta_IN", "ur": "ur_PK", "sw": "sw_KE"}

def babel_bilan_vaqt_olish(joy_nomi, til_kodi="uz"):
    try:
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder
        from babel.dates import format_datetime
        geolocator = Nominatim(user_agent="RAV_AI_World_Time")
        location = geolocator.geocode(joy_nomi, timeout=10)
        if location is None:
            return None
        tf = TimezoneFinder()
        timezone_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        if timezone_name is None:
            return None
        city_time = datetime.now(ZoneInfo(timezone_name))
        locale = LANGUAGES.get(til_kodi.split("-")[0].lower(), "en_US")
        try:
            vaqt_matni = format_datetime(city_time, "d MMMM y, HH:mm", locale=locale)
        except Exception:
            vaqt_matni = city_time.strftime("%d.%m.%Y %H:%M")
        shahar_nomi = location.address.split(",")[0]
        return shahar_nomi + ": " + vaqt_matni
    except Exception as e:
        print("Babel vaqt xatosi:", e)
        return None

def tilni_ai_aniqlash(savol):
    try:
        messages = [
            {"role": "system", "content": "Foydalanuvchi matnining qaysi tilda yozilganini aniqla. Javobni faqat ISO 639-1 ikki harfli til kodi korinishida yoz (masalan: uz, en, ru, it, zh, tg, fr, de). Hech qanday izoh, nuqta yoki qoshimcha soz yozma, faqat ikki harfli kodni yoz."},
            {"role": "user", "content": savol},
        ]
        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, max_tokens=200)
        javob = response.choices[0].message.content.strip().lower()
        for harf in javob:
            pass
        import re
        topilgan = re.findall(r"[a-z]{2}", javob)
        if topilgan:
            return topilgan[0]
        return "en"
    except Exception:
        return "en"

def dunyo_vaqti_olish(savol):
    ai_joy = None
    for urinish in range(6):
        ai_joy = joy_nomini_ai_topish(savol)
        if ai_joy:
            break
        time.sleep(1)
    if not ai_joy:
        ai_joy = "Tashkent"
    zona, nom = joy_vaqt_zonasi_topish(ai_joy)
    if not zona:
        zona = "Asia/Tashkent"
        nom = ai_joy
    try:
        hozir = datetime.now(ZoneInfo(zona))
        return (nom or ai_joy).title() + " hozir soat: " + hozir.strftime("%H:%M") + " (" + hozir.strftime("%d.%m.%Y") + ")"
    except Exception:
        return "Vaqtni aniqlab bolmadi"

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
    }
    for kalit, shahar in mamlakatlar.items():
        if kalit in savol_lower:
            return shahar
    shaharlar = [
        "toshkent", "samarqand", "buxoro", "namangan", "andijon",
        "dubai", "moscow", "london", "paris", "berlin",
        "tokyo", "seoul", "delhi", "istanbul", "cairo",
        "sydney", "singapore", "bangkok", "karachi", "baku",
    ]
    for shahar in shaharlar:
        if shahar in savol_lower:
            return shahar.replace(" ", "+").title()
    words = savol.replace("?","").replace("!","").replace(".","").replace(",","").split()
    stop = ["ob-havo","ob","havo","qanday","hozir","bugun","weather","harorat","iqlim","da","de","ni","ning","qanday"]
    for w in reversed(words):
        if w.lower() not in stop and len(w) > 2:
            shahar = w
            for end in ["da","de","ni","ga","dan"]:
                if shahar.lower().endswith(end) and len(shahar) > len(end)+2:
                    shahar = shahar[:-len(end)]
                    break
            return shahar.title()
    return "Tashkent"

def ob_havo_tavsif_tarjima_qil(matn_en):
    try:
        import html
        from deep_translator import MyMemoryTranslator
        kod = mymemory_til_kodi_topish("uz")
        natija = MyMemoryTranslator(source="en-GB", target=kod).translate(matn_en)
        if natija:
            natija = html.unescape(natija)
        return natija if natija else matn_en
    except Exception:
        return matn_en


def ob_havo_yorliq_tarjima_qil(soz_uz, til_kodi):
    try:
        if not til_kodi or til_kodi.lower() in ("uz", "uz-uz"):
            return soz_uz
        import html
        from deep_translator import MyMemoryTranslator
        kod = mymemory_til_kodi_topish(til_kodi)
        manba_kod = mymemory_til_kodi_topish("uz")
        natija = MyMemoryTranslator(source=manba_kod, target=kod).translate(soz_uz)
        if natija:
            natija = html.unescape(natija)
        return natija if natija else soz_uz
    except Exception:
        return soz_uz

def ob_havo_matn_tarjima_qil(matn_en, til_kodi):
    try:
        if not til_kodi or til_kodi.lower() in ("en", "en-gb", "en-us"):
            return matn_en
        import html, re
        from deep_translator import MyMemoryTranslator
        himoya_belgisi = "XSOMX9Y"
        matn_himoyalangan = re.sub(r"\bsom\b", himoya_belgisi, matn_en, flags=re.IGNORECASE)
        kod = mymemory_til_kodi_topish(til_kodi)
        natija = MyMemoryTranslator(source="en-GB", target=kod).translate(matn_himoyalangan)
        if natija:
            natija = html.unescape(natija)
            natija = natija.replace(himoya_belgisi, "som").replace(himoya_belgisi.lower(), "som").replace(himoya_belgisi.capitalize(), "Som")
        return natija if natija else matn_en
    except Exception:
        return matn_en

def ob_havo_olish(shahar, til_kodi=None):
    try:
        url = "https://wttr.in/" + shahar.replace(" ", "+") + "?format=j1"
        r = http_client.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            cur = d["current_condition"][0]
            harorat = cur["temp_C"]
            his = cur["FeelsLikeC"]
            namlik = cur["humidity"]
            shamol = cur["windspeedKmph"]
            tavsif_en = cur["weatherDesc"][0]["value"]
            weather3 = d["weather"]
            kunlar_en = ["Today", "Tomorrow", "Day after tomorrow"]
            qatorlar = []
            qatorlar.append(shahar + " weather:")
            qatorlar.append("Temperature: " + harorat + "C (feels like: " + his + "C)")
            qatorlar.append("Humidity: " + namlik + "%")
            qatorlar.append("Wind: " + shamol + " km/h")
            qatorlar.append("Condition: " + tavsif_en)
            qatorlar.append("3-day forecast:")
            for i, w in enumerate(weather3[:3]):
                min_t = w["mintempC"]
                max_t = w["maxtempC"]
                tavsif3_en = w["hourly"][4]["weatherDesc"][0]["value"]
                qatorlar.append(kunlar_en[i] + ": " + min_t + "C ~ " + max_t + "C, " + tavsif3_en)
            matn_en = chr(10).join(qatorlar)
            maqsad_til = til_kodi if til_kodi else "uz"
            return ob_havo_matn_tarjima_qil(matn_en, maqsad_til)
    except Exception as e:
        print("Ob-havo xatosi:", e)
    try:
        url = "https://wttr.in/" + shahar.replace(" ", "+") + "?format=3"
        r = http_client.get(url, timeout=5)
        if r.status_code == 200:
            return "Ob-havo: " + r.text
    except:
        pass
    return ""
def internet_qidirish(savol):
    natija = ""
    if kerak_mi_yangilik(savol):
        mavzu = yangilik_mavzusi(savol)
        yangiliklar = yangiliklar_olish(mavzu)
        if yangiliklar:
            natija += "Yangiliklar:" + "".join([f"{i+1}. {y[:80]}" for i, y in enumerate(yangiliklar[:3])])
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
        system += "\nInternet malumotlari:\n" + internet_malumot
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

@app.post(f"/telegram/{TELEGRAM_TOKEN}")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        threading.Thread(target=telegram_xabar_qayta_ishlash, args=(update,), daemon=True).start()
    except Exception as e:
        print("Webhook xato:", e)
    return {"ok": True}

MYMEMORY_TILLAR_KESH = None

def mymemory_til_kodi_topish(til_kodi):
    global MYMEMORY_TILLAR_KESH
    from deep_translator import MyMemoryTranslator
    if MYMEMORY_TILLAR_KESH is None:
        try:
            MYMEMORY_TILLAR_KESH = MyMemoryTranslator(source="en-GB", target="en-GB").get_supported_languages(as_dict=True)
        except Exception:
            MYMEMORY_TILLAR_KESH = {}
    til_kodi = til_kodi.lower()
    qolda_mos = {
        "zh-cn": "zh-CN", "zh": "zh-CN", "pt-br": "pt-BR",
    }
    if til_kodi in qolda_mos:
        return qolda_mos[til_kodi]
    for nom, kod in MYMEMORY_TILLAR_KESH.items():
        if kod.lower() == til_kodi or kod.lower().startswith(til_kodi + "-"):
            return kod
    return til_kodi

OB_HAVO_LABELLAR = ["Harorat:", "his:", "Namlik:", "Shamol:", "Holat:", "3 kunlik:", "Bugun:", "Ertaga:", "Indinga:"]

def ob_havo_tarjima_qil(matn, til_kodi):
    try:
        tarjima_kesh = {}
        natija = matn
        for label in OB_HAVO_LABELLAR:
            if label in natija:
                if label not in tarjima_kesh:
                    t = deep_tarjima_qil(label, til_kodi)
                    tarjima_kesh[label] = t if t else label
                natija = natija.replace(label, tarjima_kesh[label])
        return natija
    except Exception as e:
        print("Ob-havo tarjima xatosi:", e)
        return None

def ob_havo_toliq_tarjima_qil(matn, til_kodi):
    try:
        majburiy_til = "uz" if (not til_kodi or til_kodi.lower() in ("uz", "uz-uz")) else til_kodi
        from deep_translator import MyMemoryTranslator
        import html, re
        himoya_belgisi = "XSOMX9Y"
        matn_himoyalangan = re.sub(r"\bsom\b", himoya_belgisi, matn, flags=re.IGNORECASE)
        kod = mymemory_til_kodi_topish(majburiy_til)
        natija = MyMemoryTranslator(source="en-GB", target=kod).translate(matn_himoyalangan)
        if natija:
            natija = html.unescape(natija)
            natija = natija.replace(himoya_belgisi, "som").replace(himoya_belgisi.lower(), "som").replace(himoya_belgisi.capitalize(), "Som")
        if not natija:
            return matn
        qolgan_ozbekcha = ["Bugun:", "Ertaga:", "Indinga:", "kunlik"]
        if any(s in natija for s in qolgan_ozbekcha):
            natija = ob_havo_tarjima_qil(natija, til_kodi)
        return natija
    except Exception as e:
        print("Ob-havo toliq tarjima xatosi:", e)
        return matn

def deep_tarjima_qil(matn, til_kodi):
    try:
        if til_kodi and til_kodi.lower() in ("uz", "uz-uz"):
            return matn
        from deep_translator import MyMemoryTranslator
        import html, re
        himoya_belgisi = "XSOMX9Y"
        matn_himoyalangan = re.sub(r"\bsom\b", himoya_belgisi, matn, flags=re.IGNORECASE)
        kod = mymemory_til_kodi_topish(til_kodi)
        natija = MyMemoryTranslator(source="en-GB", target=kod).translate(matn_himoyalangan)
        if natija:
            natija = html.unescape(natija)
            natija = natija.replace(himoya_belgisi, "som").replace(himoya_belgisi.lower(), "som").replace(himoya_belgisi.capitalize(), "Som")
        return natija
    except Exception as e:
        print("Deep-translator xatosi:", e)
        return None

def javobni_tarjima_qil(javob_matni, asl_savol):
    for urinish in range(3):
        try:
            messages = [
                {"role": "system", "content": "Foydalanuvchi savolining aniq qaysi tilda va qaysi alifboda yozilganini aniqla. Keyin berilgan MATNNI (vaqt, obhavo yoki valyuta natijasi) TOLIQ va BUTUNLAY aynan osha tilga va osha alifboga tarjima qil. MUHIM: matndagi BARCHA sozlarni tarjima qil, jumladan yorliq sozlarni ham (masalan Harorat, Namlik, Shamol, Holat, Bugun, Ertaga kabi sozlarning barchasini ham tarjima qil) - hech bitta ozbekcha yoki boshqa til sozi qolib ketmasin. Sonlar, foiz belgisi, gradus belgisi va shahar nomlarini ozgartirma. Shahar, davlat va joy nomlarini ASLO boshqa joy nomiga almashtirma. Agar savol xitoy tilida bolsa javob TOLIQ xitoy tilida ieroglif bilan bolishi kerak, bironta ham ozbekcha soz qolmasligi kerak. Faqat tarjima qilingan natija matnini yoz, hech qanday izoh yozma, savolni takrorlama."},
                {"role": "user", "content": "Savol tili aniqlanadigan matn: " + asl_savol + chr(10) + "Tarjima qilinishi kerak bolgan natija: " + javob_matni},
            ]
            response = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=800)
            natija = response.choices[0].message.content.strip()
            if natija and natija != asl_savol.strip():
                return natija
        except Exception:
            pass
        time.sleep(1)
    return javob_matni

SLENG_LUGAT = {
    "zo'r-ku": "juda yaxshi ekan",
    "zo'rku": "juda yaxshi ekan",
    "qoyil": "ajoyib",
    "qoyilmaqom": "juda ajoyib",
    "padavlat": "boy odam",
    "voy-buy": "voy, hayron qoldim",
    "voy buy": "voy, hayron qoldim",
    "lom-mim": "hech narsa",
    "lom mim": "hech narsa",
    "kaltafahm": "tushunmovchan",
    "jajji": "kichkina",
    "chakki emas": "yomon emas",
    "pachava": "juda yomon",
}


from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
rav_db = mongo_client["rav_ai_db"]
foydalanuvchilar = rav_db["foydalanuvchilar"]


def foydalanuvchini_saqla(chat_id, ism=None, shahar=None, mavzu=None):
    chat_id = str(chat_id)
    mavjud = foydalanuvchilar.find_one({"chat_id": chat_id})
    if not mavjud:
        yangi = {"chat_id": chat_id, "ism": ism, "shaharlar": {}, "mavzular": {}}
        foydalanuvchilar.insert_one(yangi)
        mavjud = yangi
    yangilash = {}
    if ism:
        yangilash["ism"] = ism
    if shahar:
        shaharlar = mavjud.get("shaharlar", {})
        shaharlar[shahar] = shaharlar.get(shahar, 0) + 1
        yangilash["shaharlar"] = shaharlar
    if mavzu:
        mavzular = mavjud.get("mavzular", {})
        mavzular[mavzu] = mavzular.get(mavzu, 0) + 1
        yangilash["mavzular"] = mavzular
    if yangilash:
        foydalanuvchilar.update_one({"chat_id": chat_id}, {"$set": yangilash})


def foydalanuvchini_olish(chat_id):
    chat_id = str(chat_id)
    return foydalanuvchilar.find_one({"chat_id": chat_id})


def sevimli_shahar_olish(chat_id):
    foydalanuvchi = foydalanuvchini_olish(chat_id)
    if not foydalanuvchi:
        return None
    shaharlar = foydalanuvchi.get("shaharlar", {})
    if not shaharlar:
        return None
    return max(shaharlar, key=shaharlar.get)

def sleng_tozala(matn):
    import re
    natija = matn
    for sleng, adabiy in SLENG_LUGAT.items():
        andoza = re.compile(re.escape(sleng), re.IGNORECASE)
        natija = andoza.sub(adabiy, natija)
    return natija


@app.post("/savol")
def savol_yuborish(data: SavolModel):
    data.matn = sleng_tozala(data.matn)
    if kerak_mi_yangilik(data.matn):
        mavzu = yangilik_mavzusi(data.matn)
        yangiliklar = yangiliklar_olish(mavzu)
        if yangiliklar:
            javob = "So'nggi yangiliklar:\n" + "\n".join([f"{i+1}. {y}" for i, y in enumerate(yangiliklar)])
            return {"javob": javob}
    kalit_ob = [
        "ob-havo", "ob havo", "havo", "weather", "harorat", "iqlim", "temps", "wetter",
        "clima", "tempo", "погода", "havo-iqlim", "天气", "mausam", "thoi tiet",
        "الطقس", "طقس", "درجة الحرارة",
        "hava durumu", "sicaklik",
        "temperature", "forecast",
        "pogoda", "pogoda dzis",
        "havo", "obhavo",
        "sydd", "veder",
        "weer", "vreme", "vrijeme", "sää", "veir", "vejr", "vader",
        "tiempo", "que tiempo hace",
        "날씨",
        "thoi tiet hom nay",
        "ilm", "eira",
        "moyin havo", "havo rayi",
    ]
    if any(s in data.matn.lower() for s in kalit_ob):
        shahar_ob = None
        for urinish_ob in range(4):
            shahar_ob = joy_nomini_ai_topish(data.matn)
            if shahar_ob:
                break
            time.sleep(1)
        if not shahar_ob:
            shahar_ob = shahar_topish(data.matn)
        til_ob = tilni_ai_aniqlash(data.matn)
        ob = ob_havo_olish(shahar_ob, til_ob)
        if ob:
            return {"javob": ob}
    if kerak_mi_valyuta(data.matn):
        kod = valyuta_kodi_topish(data.matn)
        miqdor = miqdor_topish(data.matn)
        natija = valyuta_kursi_olish(kod, miqdor)
        til_val = tilni_ai_aniqlash(data.matn)
        tarjima_val = deep_tarjima_qil(natija, til_val)
        if tarjima_val:
            return {"javob": tarjima_val}
        return {"javob": javobni_tarjima_qil(natija, data.matn)}
    if kerak_mi_vaqt(data.matn) or kerak_mi_vaqt_ai(data.matn):
        til = tilni_ai_aniqlash(data.matn)
        shahar = None
        for urinish3 in range(6):
            shahar = joy_nomini_ai_topish(data.matn)
            if shahar:
                break
            time.sleep(1)
        if not shahar:
            return {"javob": javobni_tarjima_qil("Iltimos shahar nomini aniqroq korsating.", data.matn)}
        natija = babel_bilan_vaqt_olish(shahar, til)
        if natija:
            return {"javob": natija}
        eski_natija = dunyo_vaqti_olish(data.matn)
        return {"javob": javobni_tarjima_qil(eski_natija, data.matn)}
    if kerak_mi_internet_ai(data.matn):
        qidiruv_natija = internetdan_qidirish(data.matn)
        if qidiruv_natija:
            from datetime import datetime
            bugungi_sana = datetime.now().strftime("%Y-%m-%d (%A)")
            kontekst_matn = "Bugungi sana: " + bugungi_sana + "." + chr(10) + "Quyidagi internetdan topilgan malumotlar asosida foydalanuvchi savoliga tabiiy, qisqa va aniq javob ber. Agar savolda \"kecha\", \"bugun\", \"yesterday\", \"today\" kabi nisbiy sana borsa, yuqoridagi bugungi sanaga nisbatan hisobla. Faqat kerakli malumotni ishlat, manba royxatini qaytarma." + chr(10) + chr(10) + qidiruv_natija + chr(10) + chr(10) + "Foydalanuvchi savoli: " + data.matn
            javob_internet = gemini_javob(kontekst_matn, data.session_id)
            return {"javob": javob_internet}
    javob = gemini_javob(data.matn, data.session_id)
    return {"javob": javob}

@app.post("/rasm")
def rasm_yaratish(data: RasmModel):
    try:
        prompt = rasm_prompt_tayyorla(data.matn)
        prompt_full = prompt + ", ultra realistic, 4K, professional photography, detailed"
        url = "https://image.pollinatiowi/prompt/" + prompt_full.replace(" ", "%20") + "?model=flux&width=1024&height=1024&nologo=true"
        return {"rasm_url": url}
    except Exception as e:
        return {"xato": str(e)}

# ===RAV_SCHEDULER_V3_MARKER===
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
rav_scheduler = BackgroundScheduler()
rav_scheduler.start()

import requests as rav_requests

RAV_ADMIN_CHAT_ID = '7253108810'

def rav_telegram_xabar_yubor(matn):
    try:
        token = os.getenv('TELEGRAM_TOKEN')
        url = 'https://api.telegram.org/bot' + token + '/sendMessage'
        rav_requests.post(url, json={'chat_id': RAV_ADMIN_CHAT_ID, 'text': matn})
    except Exception as xato:
        print('Telegram xabar yuborishda xato: ' + str(xato))

# ===RAV_KUNLIK_XABAR_V2===
def kunlik_xabar_yubor():
    print('[KUNLIK XABAR] boshlandi')
    try:
        ob_havo_matni = ob_havo_olish('Shirin', 'uz')
        print('[KUNLIK XABAR] ob-havo natijasi uzunligi: ' + str(len(str(ob_havo_matni))))
        print('[KUNLIK XABAR] ob-havo qiymati: ' + repr(ob_havo_matni))
        if not ob_havo_matni:
            ob_havo_matni = 'Ob-havo maʼlumoti boʼsh qaytdi (wttr.in javob bermadi)'
    except Exception as xato:
        ob_havo_matni = 'Ob-havo olishda xato: ' + str(xato)
        print('[KUNLIK XABAR] OB-HAVO XATO: ' + str(xato))
    try:
        yangiliklar_matni = internetdan_qidirish("2026-yil bugungi eng so'nggi dunyo va O'zbekiston yangiliklari")
        print('[KUNLIK XABAR] yangiliklar uzunligi: ' + str(len(str(yangiliklar_matni))))
    except Exception as xato:
        yangiliklar_matni = 'Yangiliklarni olishda xato: ' + str(xato)
        print('[KUNLIK XABAR] YANGILIK XATO: ' + str(xato))
    toliq_xabar = 'RAV AI kunlik xabar' + chr(10) + chr(10)
    toliq_xabar += 'OB-HAVO (Shirin, Sirdaryo):' + chr(10) + str(ob_havo_matni) + chr(10) + chr(10)
    toliq_xabar += 'YANGILIKLAR:' + chr(10) + str(yangiliklar_matni)
    print('[KUNLIK XABAR] Telegramga yuborilyapti...')
    rav_telegram_xabar_yubor(toliq_xabar)
    print('[KUNLIK XABAR] tugadi')

rav_scheduler.add_job(kunlik_xabar_yubor, 'cron', hour=10, minute=0, timezone='Asia/Tashkent')
print('RAV kunlik xabar (10:00, Shirin + yangiliklar) rejalashtirildi')
