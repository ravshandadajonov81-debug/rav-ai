with open("server.py", "r", encoding="utf-8") as f:
    kod = f.read()

eski_qator = 'bot_username = "ravo7_ai_bot"'
yangi_qator = 'bot_username = "ravo8_ai_bot"'

if eski_qator not in kod:
    print("mos topilmadi")
else:
    kod = kod.replace(eski_qator, yangi_qator)
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(kod)
    print("Bot username yangilandi!")