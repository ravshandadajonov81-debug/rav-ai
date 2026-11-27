with open('server.py', 'r', encoding='utf-8') as f:
    kod = f.read()

eski = 'mongo_client = MongoClient(MONGO_URI)'
yangi = 'mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)'

if eski in kod:
    kod = kod.replace(eski, yangi)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(kod)
    print("TLS sozlamasi qoshildi!")
else:
    print("DIQQAT: topilmadi.")