import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '''def javobni_tarjima_qil(javob_matni, asl_savol):
    try:
        messages = [
            {"role": "system", "content": "Foydalanuvchi savolining aniq qaysi tilda va qaysi alifboda yozilganini aniqla. Keyin berilgan matnni aynan osha tilga va osha alifboga tarjima qil. Agar savol xitoy tilida bolsa javob ham xitoy tilida ieroglif bilan bolishi kerak. Agar savol tojik tilida kirill alifbosida bolsa javob ham tojik tilida kirillcha bolishi kerak. Faqat tarjima qilingan matnni yoz hech qanday izoh yozma."},
            {"role": "user", "content": "Savol: " + asl_savol + chr(10) + "Tarjima qilinadigan matn: " + javob_matni},
        ]
        response = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=300)
        return response.choices[0].message.content.strip()
    except Exception:
        return javob_matni'''

new = '''def javobni_tarjima_qil(javob_matni, asl_savol):
    for urinish in range(3):
        try:
            messages = [
                {"role": "system", "content": "Foydalanuvchi savolining aniq qaysi tilda va qaysi alifboda yozilganini aniqla. Keyin berilgan MATNNI (vaqt yoki valyuta natijasi) aynan osha tilga va osha alifboga tarjima qil. Diqqat: savolni emas, faqat berilgan MATNNI tarjima qil va qaytar. Agar savol xitoy tilida bolsa javob ham xitoy tilida ieroglif bilan bolishi kerak. Faqat tarjima qilingan natija matnini yoz, hech qanday izoh yozma, savolni takrorlama."},
                {"role": "user", "content": "Savol tili aniqlanadigan matn: " + asl_savol + chr(10) + "Tarjima qilinishi kerak bolgan natija: " + javob_matni},
            ]
            response = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=300)
            natija = response.choices[0].message.content.strip()
            if natija and natija != asl_savol.strip():
                return natija
        except Exception:
            pass
        time.sleep(1)
    return javob_matni'''

if old in content:
    content = content.replace(old, new, 1)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")