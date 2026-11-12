import os
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

def internet_qidirish(savol):
    try:
        url = "https://wttr.in/Tashkent?format=3"
        r = http_client.get(url, timeout=5)
        if r.status_code == 200:
            return "Ob-havo: " + r.text
    except Exception as e:
        print("Ob-havo xatosi:", e)
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + savol.replace(" ", "_")
        r = http_client.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data.get("extract", "")[:500]
    except Exception as e:
        print("Wikipedia xatosi:", e)
    return ""

def kerak_mi_internet(savol):
    kalit_sozlar = ["hozir", "bugun", "yangilik", "ob-havo", "ob havo", "weather", "harorat", "narx", "qachon", "necha", "kim", "qayer", "oxirgi"]
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
        system += "\nInternet malumotlari:" + internet_malumot
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
