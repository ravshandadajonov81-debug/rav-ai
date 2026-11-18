import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '''    if kerak_mi_vaqt(data.matn) or kerak_mi_vaqt_ai(data.matn):
        natija = dunyo_vaqti_olish(data.matn)
        return {"javob": javobni_tarjima_qil(natija, data.matn)}'''

new = '''    if kerak_mi_vaqt(data.matn) or kerak_mi_vaqt_ai(data.matn):
        ai_joy2 = None
        for urinish2 in range(6):
            ai_joy2 = joy_nomini_ai_topish(data.matn)
            if ai_joy2:
                break
            time.sleep(1)
        if not ai_joy2:
            ai_joy2 = "Tashkent"
        babel_natija = babel_bilan_vaqt_olish(ai_joy2, "uz")
        if babel_natija:
            return {"javob": javobni_tarjima_qil(babel_natija, data.matn)}
        natija = dunyo_vaqti_olish(data.matn)
        return {"javob": javobni_tarjima_qil(natija, data.matn)}'''

if old in content:
    content = content.replace(old, new, 1)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")