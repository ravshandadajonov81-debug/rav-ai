import re

with open("server.py", "r", encoding="utf-8") as f:
    kod = f.read()

eski_blok = '''            else:
                javob = gemini_javob(matn, session_id)
                telegram_yuborish(chat_id, javob)'''

yangi_blok = '''            else:
                if aniq_mavzu == "ob-havo" and not aniq_shahar:
                    try:
                        sevimli = sevimli_shahar_olish(chat_id)
                        if sevimli:
                            matn = matn.strip()
                            if matn.endswith("?"):
                                matn = matn[:-1].strip()
                            matn = f"{sevimli}da {matn}?"
                    except Exception as sevimli_xato:
                        print("Sevimli shahar olish xatosi:", sevimli_xato)
                javob = gemini_javob(matn, session_id)
                telegram_yuborish(chat_id, javob)'''

if eski_blok not in kod:
    print("mos topilmadi")
else:
    kod = kod.replace(eski_blok, yangi_blok)

    funksiya_qoshish_nuqtasi = "def foydalanuvchini_olish(chat_id):"
    yangi_funksiya = '''def sevimli_shahar_olish(chat_id):
    try:
        foydalanuvchi = foydalanuvchini_olish(chat_id)
        if not foydalanuvchi:
            return None
        shaharlar = foydalanuvchi.get("shaharlar", {})
        if not shaharlar:
            return None
        eng_kop_shahar = max(shaharlar, key=shaharlar.get)
        return eng_kop_shahar
    except Exception:
        return None


def foydalanuvchini_olish(chat_id):'''

    if funksiya_qoshish_nuqtasi not in kod:
        print("funksiya nuqtasi topilmadi")
    else:
        kod = kod.replace(funksiya_qoshish_nuqtasi, yangi_funksiya, 1)
        with open("server.py", "w", encoding="utf-8") as f:
            f.write(kod)
        print("Sevimli shahar funksiyasi qoshildi!")