import server

chat_id_test = 777777

server.telegram_xabar_qayta_ishlash({
    "message": {"chat": {"id": chat_id_test, "type": "private"}, "text": "Samarqandda ob-havo qanday?"}
})

server.telegram_xabar_qayta_ishlash({
    "message": {"chat": {"id": chat_id_test, "type": "private"}, "text": "ob-havo qanday?"}
})

foydalanuvchi = server.foydalanuvchini_olish(chat_id_test)
print("Natija:", foydalanuvchi)
