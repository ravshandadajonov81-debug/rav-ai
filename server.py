import time
import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai

API_KEY = "AQ.Ab8RN6JeuRGx847ue-YoZ8qdxhMkHUjnnPVRtT7V3tnUrHqmrA"
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

@app.get("/", response_class=HTMLResponse)
def bosh_sahifa():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/savol")
def savol_yuborish(data: SavolModel):
    javob = gemini_javob(data.matn)
    return {"javob": javob}