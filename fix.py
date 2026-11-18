import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'kalit = ["dollar", "euro", "rubl", "valyuta", "kurs", "som", "narxi qancha", "qancha turadi", "valyuta kursi", "dollar kursi", "euro kursi", "exchange rate", "currency", "usd", "eur", "rub"]'

new = 'kalit = ["dollar", "euro", "rubl", "valyuta", "kurs", "som", "narxi qancha", "qancha turadi", "valyuta kursi", "dollar kursi", "euro kursi", "exchange rate", "currency"]'

if old in content:
    content = content.replace(old, new, 1)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")