f = open("server.py", "r", encoding="utf-8")
content = f.read()
f.close()

bad = '    kalit_ob = ["ob-havo", "ob havo", "havo", "weather", "harorat", "iqlim"]    if any(s in data.matn.lower() for s in kalit_ob):        shahar = shahar_topish(data.matn)        ob = ob_havo_olish(shahar)        if ob:            return {"javob": ob}    javob = gemini_javob(data.matn, data.session_id)'

good = '''    kalit_ob = ["ob-havo", "ob havo", "havo", "weather", "harorat", "iqlim"]
    if any(s in data.matn.lower() for s in kalit_ob):
        shahar = shahar_topish(data.matn)
        ob = ob_havo_olish(shahar)
        if ob:
            return {"javob": ob}
    javob = gemini_javob(data.matn, data.session_id)'''

if bad in content:
    content = content.replace(bad, good)
    print("Topildi va tuzatildi!")
else:
    print("Topilmadi! Qidiramiz...")
    import re
    pattern = r'kalit_ob = \[.*?\]\s*if any.*?kalit_ob\):\s*shahar = shahar_topish.*?\)\s*ob = ob_havo_olish.*?\)\s*if ob:\s*return \{"javob": ob\}\s*javob = gemini_javob\(data\.matn, data\.session_id\)'
    content = re.sub(pattern, good.strip(), content)
    print("Regex orqali almashtirildi!")

f = open("server.py", "w", encoding="utf-8")
f.write(content)
f.close()