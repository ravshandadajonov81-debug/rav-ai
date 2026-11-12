import os
import time
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY", "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")

http_client = httpx.Client(verify=False)
client = Groq(api_key=API_KEY, http_client=http_client)
app = FastAPI()

suhbat_tarixi = []

def gemini_javob(savol):
    global suhbat_tarixi
    suhbat_tarixi.append({"role": "user", "content": savol})
    if len(suhbat_tarixi) > 20:
        suhbat_tarixi = suhbat_tarixi[-20:]
    messages = [
        {"role": "system", "content": "Sen RAV AI degan eng aqlli shaxsiy assistantsan. Foydalanuvchi qaysi tilda yozsa, osha tilda javob ber. Suhbat tarixini eslab qol. Foydalanuvchi ismini aytsa eslab qol."}
    ] + suhbat_tarixi
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