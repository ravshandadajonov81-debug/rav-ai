import server

soxta_update = {
    "message": {
        "chat": {"id": 888888, "type": "private"},
        "text": "Toshkentda ob-havo qanday?"
    }
}

server.telegram_xabar_qayta_ishlash(soxta_update)

foydalanuvchi = server.foydalanuvchini_olish(888888)
print("Natija:", foydalanuvchi)
