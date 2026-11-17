f = open("server.py", "r", encoding="utf-8")
content = f.read()
f.close()

old = '    javob = gemini_javob(data.matn, data.session_id)'
new = '    if kerak_mi_valyuta(data.matn):' + chr(10)
new += '        kod = valyuta_kodi_topish(data.matn)' + chr(10)
new += '        return {"javob": valyuta_kursi_olish(kod)}' + chr(10)
new += '    javob = gemini_javob(data.matn, data.session_id)'

if old in content:
    content = content.replace(old, new, 1)
    print("Topildi!")
else:
    print("Topilmadi!")

f = open("server.py", "w", encoding="utf-8")
f.write(content)
f.close()