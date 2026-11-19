import server

yangi_system = """Sen valyuta aniqlovchi botsan. Foydalanuvchi matnida qaysi pul birligi (valyuta) tilga olinganini top.

Misollar:
Savol: "1 yuan som ga qancha boladi" -> Javob: CNY
Savol: "dollar kursi qancha" -> Javob: USD
Savol: "euro narxi" -> Javob: EUR
Savol: "Real Madrid kim yutdi" -> Javob: YOQ
Savol: "valyuta kurslari" -> Javob: YOQ
Savol: "rubl qancha turadi" -> Javob: RUB

Qoida: Agar matnda aniq BITTA valyuta nomi (dollar=USD, euro=EUR, rubl=RUB, yuan=CNY, funt/sterling=GBP, yen/yena=JPY, lira=TRY, dirham=AED, tenge=KZT, manat=AZN, hryvnia=UAH, rupiya=INR, von/won=KRW, frank/franc=CHF, real=BRL) bolsa, FAQAT shu kodni yoz. Aks holda FAQAT YOQ deb yoz. Boshqa hech narsa yozma."""

messages = [
    {"role": "system", "content": yangi_system},
    {"role": "user", "content": "1 yuan som ga qancha boladi"},
]

for i in range(5):
    response = server.client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, max_tokens=200, temperature=0)
    print(i+1, ":", repr(response.choices[0].message.content))