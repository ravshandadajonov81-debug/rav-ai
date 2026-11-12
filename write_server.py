content = open('server.py', 'w', encoding='utf-8')
content.write("""import os
import time
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY", "")
http_client = httpx.Client(verify=False)
client = Groq(api_key=API_KEY, http_client=http_client)
app = FastAPI()

suhbat_tarixi = []

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
        "bangladesh": "Dhaka",
        "tailand": "Bangkok", "thailand": "Bangkok",
        "vyetnam": "Hanoi", "vietnam": "Hanoi",
        "indoneziya": "Jakarta", "indonesia": "Jakarta",
        "malayziya": "Kuala+Lumpur", "malaysia": "Kuala+Lumpur",
        "filippin": "Manila", "philippines": "Manila",
        "isroil": "Tel+Aviv", "israel": "Tel+Aviv",
        "saudiya": "Riyadh", "saudi": "Riyadh",
        "qatar": "Doha", "doha": "Doha",
        "bae": "Dubai", "uae": "Dubai",
        "eron": "Tehran", "iran": "Tehran",
        "iroq": "Baghdad", "iraq": "Baghdad",
        "gretsiya": "Athens", "greece": "Athens",
        "ispaniya": "Madrid", "spain": "Madrid",
        "portugaliya": "Lisbon", "portugal": "Lisbon",
        "niderlandiya": "Amsterdam", "netherlands": "Amsterdam",
        "belgiya": "Brussels", "belgium": "Brussels",
        "shveytsariya": "Zurich", "switzerland": "Zurich",
        "avstriya": "Vienna", "austria": "Vienna",
        "shvetsiya": "Stockholm", "sweden": "Stockholm",
        "norvegiya": "Oslo", "norway": "Oslo",
        "finlandiya": "Helsinki", "finland": "Helsinki",
        "daniya": "Copenhagen", "denmark": "Copenhagen",
        "polsha": "Warsaw", "poland": "Warsaw",
        "ukraina": "Kyiv", "ukraine": "Kyiv",
        "gruziya": "Tbilisi", "georgia": "Tbilisi",
        "ozarbayjon": "Baku", "azerbaijan": "Baku",
        "armaniston": "Yerevan", "armenia": "Yerevan",
        "qirgiziston": "Bishkek", "kyrgyzstan": "Bishkek",
        "tojikiston": "Dushanbe", "tajikistan": "Dushanbe",
        "turkmaniston": "Ashgabat", "turkmenistan": "Ashgabat",
        "afgoniston": "Kabul", "afghanistan": "Kabul",
        "singapur": "Singapore", "singapore": "Singapore",
        "gonkong": "Hong+Kong", "hong kong": "Hong+Kong",
        "yangi zelandiya": "Auckland", "new zealand": "Auckland",
        "keniya": "Nairobi", "kenya": "Nairobi",
        "marokash": "Casablanca", "morocco": "Casablanca",
        "kolumbiya": "Bogota", "colombia": "Bogota",
        "venesuela": "Caracas", "venezuela": "Caracas",
        "peru": "Lima", "chili": "Santiago", "chile": "Santiago",
        "kuba": "Havana", "cuba": "Havana",
    }
    for kalit, shahar in mamlakatlar.items():
        if kalit in savol_lower:
            return shahar
    shaharlar = [
        "toshkent", "samarqand", "buxoro", "namangan", "andijon",
        "dubai", "dubay", "abu dhabi",
        "moscow", "london", "paris", "berlin", "rome", "madrid",
        "amsterdam", "vienna", "prague", "warsaw", "budapest",
        "new york", "los angeles", "chicago", "toronto", "montreal",
        "beijing", "shanghai", "tokyo", "osaka", "seoul",
        "delhi", "mumbai", "bangalore", "kolkata",
        "istanbul", "ankara", "cairo", "nairobi", "lagos",
        "sydney", "melbourne", "auckland",
        "sao paulo", "buenos aires", "bogota", "lima",
        "singapore", "bangkok", "jakarta", "kuala lumpur", "manila",
        "karachi", "lahore", "dhaka", "tehran", "baghdad",
        "kyiv", "minsk", "tbilisi", "baku", "yerevan",
        "bishkek", "dushanbe", "ashgabat", "almaty",
        "riyadh", "doha", "muscat", "kuwait", "tel aviv",
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
        system += "\\n\
Internet malumotlari:\\n" + internet_malumot
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
        url = "https://image.pollinations.ai/prompt/" + data.matn.replace(" ", "%20")
        return {"rasm_url": url}
    except Exception as e:
        return {"xato": str(e)}
""")
content.close()
print("Tayyor!")