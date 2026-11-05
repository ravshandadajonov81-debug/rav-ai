def rav_salom(ism):
    print("=========================")
    print("       RAV AI 0.2")
    print("=========================")
    print("salom,", ism.title() + "!")
    print("Men yanada aqilli bo`lib boryabman!")

foydalanuvchi = input("Ismingiz nima?")
rav_salom(foydalanuvchi)
ism = foydalanuvchi.title()

def rav_javob(savol):
    savol = savol.lower()

    if "ismim nima" in savol or "mening ismim" in savol:
        return f"sizning ismingiz {ism}!"

    elif "salom" in savol:
        return f"Salom, {ism}! Qalaysiz?"

    elif "qalaysan" in savol:
        return "Rahmat, yaxshi! Sizchi?"

    elif "isming" in savol:
        return "Mening ismim RAV AI."
    
    elif "yordam" in savol:
        return "Sizga yordam berishga tayyorman!"
    
    else:
        return "RAV AI : Bu savolni hali tushunmadim!"

print("RAV AI 0.2 ishga tushdi!")
print("Chiqish uchun stop yozing.")

while True:
    foydalanuvchi = input("Siz:")

    if foydalanuvchi.lower() == "stop":
        print("RAV AI: Xayr! Yana ko'rishamiz!")
        break
    javob = rav_javob(foydalanuvchi)
    print("RAV AI:", javob)