import io

with io.open("server.py", "r", encoding="utf-8") as f:
    kod = f.read()

marker_v3 = "# ===RAV_SCHEDULER_V3_MARKER==="
scheduler_init_belgisi = "rav_scheduler = BackgroundScheduler()"

if scheduler_init_belgisi in kod:
    print("rav_scheduler allaqachon yaratilgan, hech narsa o'zgarmadi")
elif marker_v3 not in kod:
    print("XATO: V3 marker topilmadi")
else:
    qator = chr(10)
    qoshiladigan = "from apscheduler.schedulers.background import BackgroundScheduler" + qator
    qoshiladigan += "import datetime" + qator
    qoshiladigan += "rav_scheduler = BackgroundScheduler()" + qator
    qoshiladigan += "rav_scheduler.start()" + qator

    kod = kod.replace(marker_v3, marker_v3 + qator + qoshiladigan, 1)

    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(kod)
    print("rav_scheduler qayta yaratildi va ishga tushirildi!")

print("Tuzatildi!")