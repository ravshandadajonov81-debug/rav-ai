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