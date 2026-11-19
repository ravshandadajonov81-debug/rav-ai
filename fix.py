import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

eski = '''    "von": "KRW", "won": "KRW",
    "shveytsariya franki": "CHF",
}'''

yangi = '''    "shveytsariya franki": "CHF",
}'''

if eski in content:
    content = content.replace(eski, yangi)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")