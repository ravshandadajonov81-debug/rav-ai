import io
from datetime import datetime

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

eski = '''            kontekst_matn = "Quyidagi internetdan topilgan malumotlar asosida foydalanuvchi savoliga tabiiy, qisqa va aniq javob ber. Faqat kerakli malumotni ishlat, manba royxatini qaytarma." + chr(10) + chr(10) + qidiruv_natija + chr(10) + chr(10) + "Foydalanuvchi savoli: " + data.matn'''

yangi = '''            from datetime import datetime
            bugungi_sana = datetime.now().strftime("%Y-%m-%d (%A)")
            kontekst_matn = "Bugungi sana: " + bugungi_sana + "." + chr(10) + "Quyidagi internetdan topilgan malumotlar asosida foydalanuvchi savoliga tabiiy, qisqa va aniq javob ber. Agar savolda \\"kecha\\", \\"bugun\\", \\"yesterday\\", \\"today\\" kabi nisbiy sana borsa, yuqoridagi bugungi sanaga nisbatan hisobla. Faqat kerakli malumotni ishlat, manba royxatini qaytarma." + chr(10) + chr(10) + qidiruv_natija + chr(10) + chr(10) + "Foydalanuvchi savoli: " + data.matn'''

if eski in content:
    content = content.replace(eski, yangi)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")
    