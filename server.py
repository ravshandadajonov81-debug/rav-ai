import time
import datetime
import base64
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY", "AQ.Ab8RN6ImsTfv0vDYHmnXwJmKSrKoNb6TFi__mCm6himMUZKjRg")
client = genai.Client(api_key=API_KEY)

app = FastAPI()

def gemini_javob(savol):
    kontekst = "Sen RAV AI degan aqlli shaxsiy assistantsan. O'zbek, Rus, Ingliz tillarida javob bera olasan. Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob ber."
    matn = kontekst + " Savol: " + savol
    for urinish in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=matn,
            )
            return response.text
        except Exception:
            if urinish < 2:
                time.sleep(5)
            else:
                return "Server band. Keyinroq urinib koring!"

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

import httpx

@app.post("/rasm")
def rasm_yaratish(data: RasmModel):
    try:
        url = "https://image.pollinations.ai/prompt/" + data.matn.replace(" ", "%20")
        return {"rasm_url": url}
    except Exception as e:
        return {"xato": str(e)}