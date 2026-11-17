f = open("server.py", "r", encoding="utf-8")
content = f.read()
f.close()

start_marker = 'elif matn == "/stat":'
end_marker = 'elif matn == "/yangiliklar":'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    before = content[:start_idx]
    after = content[end_idx:]
    r = ""
    r += 'elif matn == "/stat":' + chr(10)
    r += '                users = users_yuklash()' + chr(10)
    r += '                jami_user = len(users)' + chr(10)
    r += '                jami_xabar = sum(len(u.get("suhbat", [])) for u in users.values())' + chr(10)
    r += '                javob_stat = "RAV AI statistikasi:" + chr(10) + chr(10) + "Jami foydalanuvchilar: " + str(jami_user) + chr(10) + "Jami xabarlar: " + str(jami_xabar)' + chr(10)
    r += '                telegram_yuborish(chat_id, javob_stat)' + chr(10)
    r += '            '
    content = before + r + after
    print("Tuzatildi!")
else:
    print("Topilmadi!")

f = open("server.py", "w", encoding="utf-8")
f.write(content)
f.close()