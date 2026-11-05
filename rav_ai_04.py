import json
import os
import time
import datetime
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")
XOTRA_FAYILI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rav_xotira.json")
client = genai.Client(api_key=API_KEY)

def yangi_xotira():
    return {
        "shaxsiy_malumotlar": {},
        "vazifalar": [],
        "suhbat_tarixi": [],
        "eslatmalar": [],
        "maqsadlar": {},
    }

def xotirani_yuklash():
    asosiy_xotira = yangi_xotira()
    if os.path.exists(XOTRA_FAYILI):
        with open(XOTRA_FAYILI, "r", encoding="utf-8") as fayl:
            saqlangan = json.load(fayl)
        asosiy_xotira.update(saqlangan)
    return asosiy_xotira

def xotirani_saqlash(xotira):
    with open(XOTRA_FAYILI, "w", encoding="utf-8") as fayl:
        json.dump(xotira, fayl, ensure_ascii=False, indent=4)

def gemini_javob(savol, xotira):
    ism = xotira["shaxsiy_malumotlar"].get("ism", "Foydalanuvchi")
    kontekst = "Sen RAV AI degan shaxsiy assistantsan. Foydalanuvchi ismi: " + ism + ". O'zbek tilida javob ber."
    matn = kontekst + "Savol: " + savol


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

xotira = xotirani_yuklash()
xotirani_saqlash(xotira)

print("=========================")
print("       RAV AI 0.4")
print("   Gemini AI + Xotira")
print("=========================")

if xotira["shaxsiy_malumotlar"].get("ism"):
    ism = xotira["shaxsiy_malumotlar"]["ism"]
    print("RAV AI: Xush kelibsiz, " + ism + "!")
else:
    ism = input("Ismingiz nima? ")
    xotira["shaxsiy_malumotlar"]["ism"] = ism
    xotirani_saqlash(xotira)
    print("RAV AI: Salom, " + ism + "!")

print("\nVazifalaringiz:")
if xotira["vazifalar"]:
    for i, v in enumerate(xotira["vazifalar"], 1):
        print(str(i) + ". " + v)
else:
    print("   Hozircha vazifa yoq.")

print("RAV AI Chatbot (chiqish uchun xayr)")

print("-" * 40)

while True:
    savol = input("\nSiz: ").strip()

    if not savol:
        continue

    if savol.lower() in ["xayr", "bye", "chiqish"]:
        print("RAV AI: Xayr! Yana murojaat qiling!")
        xotirani_saqlash(xotira)
        break

    elif "yangi vazifa" in savol.lower() or "vazifa qosh" in savol.lower():
        v = input("Vazifani kiriting: ")
        xotira["vazifalar"].append(v)
        xotirani_saqlash(xotira)
        print("RAV AI: " + v + " qoshildi!")

    elif "vazifa" in savol.lower():
        if xotira["vazifalar"]:
            print("RAV AI: Vazifalaringiz:")
            for i, v in enumerate(xotira["vazifalar"], 1):
                print(str(i) + ". " + v)
        else:
            print("RAV AI: Vazifa yoq!")

    else:
        print("RAV AI: Oylanmoqda...")
        javob = gemini_javob(savol, xotira)
        print("RAV AI: " + str(javob))

    xotira["suhbat_tarixi"].append({
        "savol": savol,
        "vaqt": datetime.datetime.now().strftime("%H:%M")
    })
    xotirani_saqlash(xotira)