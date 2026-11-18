import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

eski = '''def kerak_mi_valyuta(savol):
    kalit = ["dollar", "euro", "rubl", "valyuta", "kurs", "som", "narxi qancha", "qancha turadi", "valyuta kursi", "dollar kursi", "euro kursi", "exchange rate", "currency"]
    return any(k in savol.lower() for k in kalit)'''

yangi = '''def kerak_mi_valyuta(savol):
    kalit = [
        "dollar", "euro", "rubl", "valyuta", "kurs", "som",
        "narxi qancha", "qancha turadi", "valyuta kursi", "dollar kursi", "euro kursi",
        "exchange rate", "currency",
        "курс", "доллар", "рубл", "валюта", "евро",
        "tasso di cambio", "valuta", "dollaro", "quanto costa il dollaro",
        "taux de change", "devise",
        "wechselkurs", "wahrung",
        "tipo de cambio", "divisa",
        "汇率", "美元", "货币",
        "exchange", "kurz meny", "kurs walut",
    ]
    return any(k in savol.lower() for k in kalit)'''

if eski in content:
    content = content.replace(eski, yangi)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")