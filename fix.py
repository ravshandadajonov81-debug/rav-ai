f = open("server.py", "r", encoding="utf-8")
content = f.read()
f.close()

old = 'def foydalanuvchi_olish(session_id):' + chr(10) + '    if session_id not in users:'
new = 'def foydalanuvchi_olish(session_id):' + chr(10) + '    users = users_yuklash()' + chr(10) + '    if session_id not in users:'

if old in content:
    content = content.replace(old, new, 1)
    print("Tuzatildi!")
else:
    print("Topilmadi!")

f = open("server.py", "w", encoding="utf-8")
f.write(content)
f.close()