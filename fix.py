f = open("server.py", "r", encoding="utf-8")
content = f.read()
f.close()

old = '    javob = gemini_javob(data.matn, data.session_id)'
new = '    if kerak_mi_vaqt(data.matn):' + chr(10)
new += '        return {"javob": dunyo_vaqti_olish(data.matn)}' + chr(10)
new += '    javob = gemini_javob(data.matn, data.session_id)'

if old in content:
    content = content.replace(old, new, 1)
    print("Topildi!")
else:
    print("Topilmadi!")

f = open("server.py", "w", encoding="utf-8")
f.write(content)
f.close()

f = open("requirements.txt", "r", encoding="utf-8")
req = f.read()
f.close()

if "tzdata" not in req:
    req += chr(10) + "tzdata" + chr(10)
    f = open("requirements.txt", "w", encoding="utf-8")
    f.write(req)
    f.close()
    print("tzdata requirements.txt ga qoshildi!")
else:
    print("tzdata allaqachon bor!")
    import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '''def dunyo_vaqti_olish(savol):
    words = savol.replace('?','').replace('!','').replace('.','').replace(',','').split()'''

new = '''def dunyo_vaqti_olish(savol):
    xitoy_shaharlar = {
        "\u4f0a\u65af\u5766\u5e03\u5c14": "Istanbul",
        "\u83ab\u65af\u79d1": "Moskva",
        "\u4f26\u6566": "London",
        "\u4e1c\u4eac": "Tokyo",
        "\u5317\u4eac": "Beijing",
        "\u6c64\u4ec0\u5e72": "Tashkent",
    }
    for k, v in xitoy_shaharlar.items():
        if k in savol:
            zona2, nom2 = joy_vaqt_zonasi_topish(v)
            if not zona2:
                zona2 = "Asia/Tashkent"
                nom2 = v
            hozir2 = datetime.now(ZoneInfo(zona2))
            return (nom2 or v).title() + "da hozir soat: " + hozir2.strftime("%H:%M") + " (" + hozir2.strftime("%d.%m.%Y") + ")"
    words = savol.replace('?','').replace('!','').replace('.','').replace(',','').split()'''

if old in content:
    content = content.replace(old, new)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")