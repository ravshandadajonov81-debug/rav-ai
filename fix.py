f = open("server.py", "r", encoding="utf-8")
content = f.read()
f.close()

old = 'message = update.get("message", {})'
new = '''message = update.get("message", {})
        chat_type = message.get("chat", {}).get("type", "private")
        bot_username = "ravo7_ai_bot"
        if chat_type in ["group", "supergroup"]:
            matn_raw = message.get("text", "")
            if ("@" + bot_username) not in matn_raw and not matn_raw.startswith("/"):
                return
            message["text"] = matn_raw.replace("@" + bot_username, "").strip()'''

if old in content:
    content = content.replace(old, new, 1)
    print("Topildi!")
else:
    print("Topilmadi!")

f = open("server.py", "w", encoding="utf-8")
f.write(content)
f.close()