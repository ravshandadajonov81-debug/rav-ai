import server

asl_yuborish = server.telegram_yuborish
def soxta_yuborish(chat_id, matn):
    print(f"BOT JAVOBI ({chat_id}): {matn}")
server.telegram_yuborish = soxta_yuborish

chat_id_test = 777777

server.telegram_xabar_qayta_ishlash({
    "message": {"chat": {"id": chat_id_test, "type": "private"}, "text": "ob-havo qanday?"}
})

server.telegram_yuborish = asl_yuborish
