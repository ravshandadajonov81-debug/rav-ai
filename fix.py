with open('server.py', 'r', encoding='utf-8') as f:
    kod = f.read()

eski = '''            try:
                foydalanuvchini_saqla(chat_id)
            except Exception as mongo_xato:
                print("Mongo saqlash xatosi:", mongo_xato)'''

yangi = '''            try:
                aniq_shahar = None
                try:
                    aniq_shahar = joy_nomini_ai_topish(matn)
                except Exception:
                    aniq_shahar = None
                aniq_mavzu = "umumiy"
                matn_kichik = matn.lower()
                if any(s in matn_kichik for s in ["ob-havo", "ob havo", "havo", "weather", "harorat"]):
                    aniq_mavzu = "ob-havo"
                elif any(s in matn_kichik for s in ["valyuta", "kurs", "dollar", "som", "rubl"]):
                    aniq_mavzu = "valyuta"
                elif any(s in matn_kichik for s in ["vaqt", "soat", "time"]):
                    aniq_mavzu = "vaqt"
                aniq_ism = None
                if "ismim" in matn_kichik:
                    soz_royxati = matn.split()
                    for i2, s2 in enumerate(soz_royxati):
                        if s2.lower().startswith("ismim") and i2 + 1 < len(soz_royxati):
                            aniq_ism = soz_royxati[i2 + 1].strip(".,!")
                            break
                foydalanuvchini_saqla(chat_id, ism=aniq_ism, shahar=aniq_shahar, mavzu=aniq_mavzu)
            except Exception as mongo_xato:
                print("Mongo saqlash xatosi:", mongo_xato)'''

if eski in kod:
    kod = kod.replace(eski, yangi)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(kod)
    print("Avtomatik aniqlash qoshildi!")
else:
    print("DIQQAT: topilmadi.")