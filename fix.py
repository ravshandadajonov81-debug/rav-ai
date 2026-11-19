import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

eski = '''def kerak_mi_valyuta(savol):
    kalit = [
        "dollar", "euro", "rubl", "valyuta", "kurs", "som",
        "narxi qancha", "qancha turadi", "valyuta kursi", "dollar kursi", "euro kursi",
        "exchange rate", "currency",
        "курс", "доллар", "рубл", "валюта", "евро",
        "tasso di cambio", "valuta", "dollaro", "quanto costa il dollaro",
        "taux de change", "devise",
        "wechselkurs", "wahrung",
        "tipo de cambio", "divisa", "cuanto vale el dolar", "cuanto vale",
        "汇率", "美元", "货币",
        "exchange", "kurz meny", "kurs walut",
        "سعر الدولار", "سعر الصرف", "الدولار", "عملة",
        "환율", "달러", "원화",
        "yuan", "yen", "lira", "dirham", "tenge", "manat", "hryvnia", "rupiya",
        "won", "franc", "real",
        "câu hỏi tỷ giá", "ty gia", "tỷ giá",
        "nilai tukar", "kurs mata uang",
    ]
    return any(k in savol.lower() for k in kalit)'''

yangi = '''VALYUTA_UMUMIY_SOZLAR = [
    "valyuta", "kurs", "exchange rate", "currency", "курс", "валюта",
    "tasso di cambio", "valuta", "taux de change", "devise",
    "wechselkurs", "wahrung", "tipo de cambio", "divisa",
    "汇率", "货币", "exchange", "kurs walut",
    "سعر الصرف", "عملة", "환율", "nilai tukar", "kurs mata uang",
]

def kerak_mi_valyuta(savol):
    savol_l = savol.lower()
    if any(s in savol_l for s in VALYUTA_UMUMIY_SOZLAR):
        return True
    for soz in VALYUTA_ISHONCHLI_SOZLAR:
        if soz in savol_l:
            return True
    for soz in VALYUTA_NOANIQ_SOZLAR:
        if soz in savol_l:
            if any(blok in savol_l for blok in VALYUTA_NOANIQ_BLOKLOVCHI):
                return False
            return True
    return False'''

if eski in content:
    content = content.replace(eski, yangi)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")