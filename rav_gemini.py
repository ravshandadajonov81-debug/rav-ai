import time
from google import genai

API_KEY = "AQ.Ab8RN6JeuRGx847ue-YoZ8qdxhMkHUjnnPVRtT7V3tnUrHqmrA"

client = genai.Client(api_key=API_KEY)

print("=========================")
print("   RAV AI — Gemini Mode")
print("=========================")
print("Chiqish uchun 'xayr' yozing\n")

while True:
    savol = input("Siz: ").strip()

    if not savol:
        continue

    if savol.lower() in ["xayr", "bye", "chiqish"]:
        print("RAV AI: Xayr! 👋")
        break

    # 3 marta urinib ko'radi
    for urinish in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=savol,
            )
            print(f"RAV AI: {response.text}")
            break
        except Exception as e:
            if urinish < 2:
                print(f"⏳ Server band, {5} soniya kutilmoqda...")
                time.sleep(5)
            else:
                print("⚠️ Server hozir band. Keyinroq urinib ko'ring!")
                