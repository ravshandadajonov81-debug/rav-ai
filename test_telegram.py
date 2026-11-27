import server

soxta_update = {
    "message": {
        "chat": {"id": 999999, "type": "private"},
        "text": "bu kino zo'r-ku, qoyil!"
    }
}

server.telegram_xabar_qayta_ishlash(soxta_update)

foydalanuvchi = server.foydalanuvchini_olish(999999)
print("MongoDB dagi foydalanuvchi:", foydalanuvchi)
