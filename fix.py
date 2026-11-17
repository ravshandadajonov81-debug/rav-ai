import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '''def dunyo_vaqti_olish(savol):'''

new = '''def joy_nomini_ai_topish(savol):
    try:
        messages = [
            {"role": "system", "content": "Foydalanuvchi matnidan faqat shahar yoki davlat nomini ajrat va shuni lotin harflarida yoz (masalan: Istanbul, Rome, New York, Moscow). Agar joy nomi topilmasa, faqat NONE deb yoz. Boshqa hech qanday izoh yozma, faqat shahar nomi yoki NONE."},
            {"role": "user", "content": savol},
        ]
        response = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=20)
        joy = response.choices[0].message.content.strip()
        if joy.upper() == "NONE" or len(joy) < 2:
            return None
        return joy
    except Exception:
        return None

def dunyo_vaqti_olish(savol):
    ai_joy = joy_nomini_ai_topish(savol)
    if ai_joy:
        zona4, nom4 = joy_vaqt_zonasi_topish(ai_joy)
        if zona4:
            hozir4 = datetime.now(ZoneInfo(zona4))
            return (nom4 or ai_joy).title() + "da hozir soat: " + hozir4.strftime("%H:%M") + " (" + hozir4.strftime("%d.%m.%Y") + ")"'''

if old in content:
    content = content.replace(old, new, 1)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")