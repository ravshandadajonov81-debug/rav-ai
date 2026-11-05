print("================================")
print("       RAV AI 0.1")
print("  Sizning aqlli yordamchingiz")
print("================================")
print("Salom! Men RAV AI man.")
print("Chiqish uchun: stop deb yozing.")

while True:
    savol = input("\nSiz: ").lower()

    if savol == "stop":
        print("RAV AI: Xayr! Yana ko'rishamiz.")
        break

    elif "salom" in savol:
        print("RAV AI: Salom! Qalaysiz?")

    elif "isming" in savol:
        print("RAV AI: Mening ismim RAV AI.")

    elif "qalaysan" in savol:
        print("RAV AI: Rahmat, yaxshi! Sizchi?")

    elif "yordam" in savol:
        print("RAV AI: Siz bilan suhbatlashishga tayyorman!")

    elif "nima qila olasan" in savol:
        print("RAV AI: Men siz bilan suhbatlasha olaman!")

    elif "nima qila olasan" in savol:
        print("RAV AI: Savollaringizga javob berishga harakat qilaman.")

    elif "nima qila olasan" in savol:
        print("RAV AI: Kelajakda yanada aqlli bo'laman!")

    else:
        print("RAV AI: Bu savolga hali javob berishni o'rganmadim.")
