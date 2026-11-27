import io

with io.open("server.py", "r", encoding="utf-8") as f:
    kod = f.read()

eski_funksiya_belgisi = "def kunlik_xabar_yubor():"
yangi_marker = "# ===RAV_KUNLIK_XABAR_V2==="

if yangi_marker in kod:
    print("Kunlik xabar V2 (log bilan) allaqachon qo'shilgan")
elif eski_funksiya_belgisi not in kod:
    print("XATO: kunlik_xabar_yubor funksiyasi topilmadi")
else:
    qator = chr(10)

    yangi_funksiya = yangi_marker + qator
    yangi_funksiya += "def kunlik_xabar_yubor():" + qator
    yangi_funksiya += "    print('[KUNLIK XABAR] boshlandi')" + qator
    yangi_funksiya += "    try:" + qator
    yangi_funksiya += "        ob_havo_matni = ob_havo_olish('Shirin')" + qator
    yangi_funksiya += "        print('[KUNLIK XABAR] ob-havo natijasi uzunligi: ' + str(len(str(ob_havo_matni))))" + qator
    yangi_funksiya += "        print('[KUNLIK XABAR] ob-havo qiymati: ' + repr(ob_havo_matni))" + qator
    yangi_funksiya += "        if not ob_havo_matni:" + qator
    yangi_funksiya += "            ob_havo_matni = 'Ob-havo maʼlumoti boʼsh qaytdi (wttr.in javob bermadi)'" + qator
    yangi_funksiya += "    except Exception as xato:" + qator
    yangi_funksiya += "        ob_havo_matni = 'Ob-havo olishda xato: ' + str(xato)" + qator
    yangi_funksiya += "        print('[KUNLIK XABAR] OB-HAVO XATO: ' + str(xato))" + qator
    yangi_funksiya += "    try:" + qator
    yangi_funksiya += "        yangiliklar_matni = internetdan_qidirish(\"bugungi asosiy dunyo va O'zbekiston yangiliklari\")" + qator
    yangi_funksiya += "        print('[KUNLIK XABAR] yangiliklar uzunligi: ' + str(len(str(yangiliklar_matni))))" + qator
    yangi_funksiya += "    except Exception as xato:" + qator
    yangi_funksiya += "        yangiliklar_matni = 'Yangiliklarni olishda xato: ' + str(xato)" + qator
    yangi_funksiya += "        print('[KUNLIK XABAR] YANGILIK XATO: ' + str(xato))" + qator
    yangi_funksiya += "    toliq_xabar = 'RAV AI kunlik xabar' + chr(10) + chr(10)" + qator
    yangi_funksiya += "    toliq_xabar += 'OB-HAVO (Shirin, Sirdaryo):' + chr(10) + str(ob_havo_matni) + chr(10) + chr(10)" + qator
    yangi_funksiya += "    toliq_xabar += 'YANGILIKLAR:' + chr(10) + str(yangiliklar_matni)" + qator
    yangi_funksiya += "    print('[KUNLIK XABAR] Telegramga yuborilyapti...')" + qator
    yangi_funksiya += "    rav_telegram_xabar_yubor(toliq_xabar)" + qator
    yangi_funksiya += "    print('[KUNLIK XABAR] tugadi')" + qator

    boshi, qolgani = kod.split(eski_funksiya_belgisi, 1)

    qatorlar = qolgani.split(qator)
    yakunlovchi_qator_indeksi = None
    for i in range(1, len(qatorlar)):
        satr = qatorlar[i]
        if satr.strip() == "" or satr.startswith("    ") or satr.startswith(chr(9)):
            continue
        else:
            yakunlovchi_qator_indeksi = i
            break

    if yakunlovchi_qator_indeksi is None:
        qolgan_qism = ""
    else:
        qolgan_qism = qator.join(qatorlar[yakunlovchi_qator_indeksi:])

    kod = boshi.rstrip() + qator + qator + yangi_funksiya + qator + qolgan_qism

    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(kod)
    print("kunlik_xabar_yubor funksiyasiga batafsil log qo'shildi!")

print("Tuzatildi!")