print("================================")
print("       RAV AI 0.1")
print("  Sizning aqlli yordamchingiz")
print("================================")
print("Salom! Men RAV AI man.")
print("Chiqish uchun: stop deb yozing.")

import json
import os

xotra = {}

if os.path.exists("rav_xotra.json"):
    with open("rav_xotra.json", "r", encoding="utf-8") as f:
        xotra = json.load(f)

isim = xotra.get("ism", "")
rang = xotra.get("rang", "")
mashina = xotra.get("mashina", "")
sport = xotra.get("sport", "")
shahar = xotra.get("shahar", "")
            
while True:
    savol = input("\nSiz: ").lower()

    if savol == "stop":
        print("RAV AI: Xayr! Yana ko'rishamiz.")
        break

    elif "mening ismim" in savol:
        isim = savol.replace("mening ismim","").strip()

        xotra["ism"] = isim

        with open("rav_xotra.json", "w", encoding="utf-8") as f:
            json.dump( xotra, f, ensure_ascii=False, indent=4)

        print("RAV AI: Tanishganimdan xursandman", isim.title())   
         
    elif "mening sevimli rangim" in savol:
        rang = savol.replace("mening sevimli rangim","").strip()

        xotra["rang"] = rang

        with open("rav_xotra.json", "w", encoding="utf-8") as f:
            json.dump(xotra, f, ensure_ascii=False, indent=4)

        print("RAV AI: Sevimli rangingizni eslab qoldim:", rang)

    elif "menga" in savol and "yoqadi" in savol:
        mashina = savol.replace("menga","").replace("yoqadi","").strip()

        xotra["mashina"] = mashina

        with open("rav_xotra.json", "w", encoding="utf-8") as f:
            json.dump(xotra, f, ensure_ascii=False, indent=4)

        print("RAV AI: Yaxshi tanlov! Buni eslab qoldim:", mashina.title())

    elif "mashinam nima" in savol:
        if mashina != "":
            print("RAV AI: Siz yoqtirgan mashina", mashina.title())
        else:
            print("RAV AI: Hali mashinangizni aytmadingiz.") 

    elif "mening sevimli sportim" in savol:
        sport = savol.replace("mening sevimli sportim","").strip()

        xotra["sport"] = sport

        with open("rav_xotra.json", "w", encoding="utf-8") as f:
            json.dump(xotra, f, ensure_ascii=False, indent=4)

        print("RAV AI: Sevimli sportingizni eslab qoldim:", sport.title())

    elif "sevimli sportim nima" in savol:
        if sport != "":
            print("RAV AI: Sizning sevimli sportingiz", sport.title())
        else:
            print("RAV AI: Hali sevimli sportingizni aytmadingiz.")
            
    elif "sevimli rangim nima" in savol:
        if rang != "":
            print("RAV AI: Sizning sevimli rangingiz", rang)
        else:
            print("RAV AI: Hali sevimli rangingizni aytmadingiz.")

    elif"ismim nima" in savol:
        if isim != "":
            print("RAV AI: Sizning ismingiz", isim.title())
        else:
            print("RAV AI: Hali ismingizni aytmadingiz.")

    elif "+" in savol:
        try:
            sonlar = savol.split("+")
            son1 = float(sonlar[0])
            son2 = float(sonlar[1])
            print("RAV AI: Natija:", son1 + son2)
        except (ValueError, IndexError):
            print("RAV AI: Iltimos, faqat son kiriting.")

    elif "-" in savol:
        try:
            sonlar = savol.split("-")
            son1 = float(sonlar[0])
            son2 = float(sonlar[1])
            print("RAV AI: Natija:", son1 - son2)
        except (ValueError, IndexError):
            print("RAV AI: Iltimos, faqat son kiriting.")

    elif "*" in savol:
        try:
            sonlar = savol.split("*")
            son1 = float(sonlar[0])
            son2 = float(sonlar[1])
            print("RAV AI: Natija:", son1 * son2)
        except (ValueError, IndexError):
            print("RAV AI: Iltimos, faqat son kiriting.")  

    elif "/" in savol:
        try:
            sonlar = savol.split("/")
            son1 = float(sonlar[0])
            son2 = float(sonlar[1])

            if son2 == 0:
                print("RAV AI: Noldan bo'lish mumkin emas.")
            else:
                print("RAV AI: Natija:", son1 / son2)
        except (ValueError, IndexError):
            print("RAV AI: Iltimos, faqat son kiriting.")

    elif "salom" in savol:
        if isim != "":
            print("RAV AI: Salom,", isim.title() + "!")
        else:
            print("RAV AI: Salom! Qalaysiz?")           

    elif "rahmat" in savol:
        if isim != "":
            print("RAV AI: Arzimaydi,", isim.title() + "!")
        else:
            print("RAV AI: Arzimaydi!")    

    elif "isming" in savol:
        print("RAV AI: Mening ismim RAV AI.") 

    elif "qalaysan" in savol:
        print("RAV AI: Rahmat, yaxshi! Sizchi?")

    elif "yordam" in savol:
        print("RAV AI: Siz bilan suhbatlashishga tayyorman!")

    elif "nima qila olasan" in savol:
        print("RAV AI: Men siz bilan suhbatlasha olaman!")
        print("RAV AI: Savollaringizga javob berishga harakat qilaman.")
        print("RAV AI: Kelajakda yanada aqlli bo'laman!")    

    else:
        print("RAV AI: Bu savolga hali javob berishni o'rganmadim.")
