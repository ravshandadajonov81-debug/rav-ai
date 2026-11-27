with open('server.py', 'r', encoding='utf-8') as f:
    kod = f.read()

eski = '''        chat_id = message.get("chat", {}).get("id")
        matn = message.get("text", "")
        if chat_id and matn:
            session_id = f"telegram_{chat_id}"'''

yangi = '''        chat_id = message.get("chat", {}).get("id")
        matn = message.get("text", "")
        if chat_id and matn:
            matn = sleng_tozala(matn)
            message["text"] = matn
            try:
                foydalanuvchini_saqla(chat_id)
            except Exception as mongo_xato:
                print("Mongo saqlash xatosi:", mongo_xato)
            session_id = f"telegram_{chat_id}"'''

if eski in kod:
    kod = kod.replace(eski, yangi)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(kod)
    print("Telegram ga sleng va MongoDB integratsiya qilindi!")
else:
    print("DIQQAT: mos qator topilmadi.")