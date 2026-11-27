import io

with io.open("server.py", "r", encoding="utf-8") as f:
    kod = f.read()

eski_qator = "ob_havo_matni = ob_havo_olish('Shirin')"
yangi_qator = "ob_havo_matni = ob_havo_olish('Shirin', 'uz')"

eski_qidiruv = 'internetdan_qidirish("bugungi asosiy dunyo va O\'zbekiston yangiliklari")'
yangi_qidiruv = 'internetdan_qidirish("2026-yil bugungi eng so\'nggi dunyo va O\'zbekiston yangiliklari")'

ozgardimi = False

if eski_qator in kod:
    kod = kod.replace(eski_qator, yangi_qator)
    print("Ob-havo tiliga uz qoshildi!")
    ozgardimi = True
else:
    print("Ob-havo qatori topilmadi (balki allaqachon tuzatilgan)")

if eski_qidiruv in kod:
    kod = kod.replace(eski_qidiruv, yangi_qidiruv)
    print("Yangiliklar so'rovi aniqlashtirildi!")
    ozgardimi = True
else:
    print("Yangiliklar qatori topilmadi (balki allaqachon tuzatilgan)")

if ozgardimi:
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(kod)
    print("server.py saqlandi!")

print("Tuzatildi!")