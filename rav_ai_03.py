import json
import os

XOTRA_FAYILI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rav_xotira.json")


def yangi_xotira():
    return {
        "shaxsiy_malumotlar": {},
        "oilaviy_malumotlar": {},
        "dostlar": {},
        "qiziqishlar": {},
        "sevimli_narsalar": {},
        "maqsadlar": {},
        "ish_va_talim": {},
        "loyihalar": {},
        "suhbat_tarixi": [],
        "vazifalar": [],
        "eslatmalar": [],
        "kunlik_reja": [],
        "muhim_sanalar": {},
        "sozlamalar": {},
        "til_sozlamalari": {},
        "foydalanuvchi_talablari": {},
        "xotira_tarixi": [],
    }


def xotirani_yuklash():
    asosiy_xotira = yangi_xotira()

    if os.path.exists(XOTRA_FAYILI):
        with open(XOTRA_FAYILI, "r", encoding="utf-8") as fayl:
            saqlangan_xotira = json.load(fayl)

        if "shaxsiy_malumotlar" in saqlangan_xotira:
            saqlangan_xotira["shaxsiy_malumotlar"] = saqlangan_xotira.pop("shaxsiy_malumotlar")

        if "loyihalar" in saqlangan_xotira:
            saqlangan_xotira["loyihalar"] = saqlangan_xotira.pop("loyihalar")

        if "foydalanuvchi_talablari" in saqlangan_xotira:
            saqlangan_xotira["foydalanuvchi_talablari"] = saqlangan_xotira.pop("foydalanuvchi_talablari")

        asosiy_xotira.update(saqlangan_xotira)

    return asosiy_xotira


def xotirani_saqlash(xotira):
    with open(XOTRA_FAYILI, "w", encoding="utf-8") as fayl:
        json.dump(xotira, fayl, ensure_ascii=False, indent=4)


# =========================
# ASOSIY DASTUR
# =========================
xotira = xotirani_yuklash()
xotirani_saqlash(xotira)

print("=========================")
print("       RAV AI 0.3")
print("=========================")
print("Xotira tizimi ishga tushdi!")

# Ismni tekshirish — oldin kelganmi?
if xotira["shaxsiy_malumotlar"].get("ism"):
    ism = xotira["shaxsiy_malumotlar"]["ism"]
    print(f"\nRAV AI: Xush kelibsiz yana, {ism}! ")
    print("RAV AI: Sizni tanidim, chunki xotiram bor! ")
else:
    ism = input("Ismingiz nima? ")
    xotira["shaxsiy_malumotlar"]["ism"] = ism
    xotirani_saqlash(xotira)
    print(f"RAV AI: Salom, {ism}! ")
    print("RAV AI: Ismingiz xotiraga saqlandi! ")

if not xotira["shaxsiy_malumotlar"].get("yosh"):
    yosh = input("Yoshingiz necha? ")
    xotira["shaxsiy_malumotlar"]["yosh"] = yosh
    xotirani_saqlash(xotira)
    print(f"RAV AI: {yosh} yoshdasiz, yaxshi! ")

if not xotira["shaxsiy_malumotlar"].get("telefon"):
    telefon = input("Telefon raqamingiz? ")
    xotira["shaxsiy_malumotlar"]["telefon"] = telefon
    xotirani_saqlash(xotira)
    print("RAV AI: Telefon raqamingiz saqlandi! ")

if not xotira["shaxsiy_malumotlar"].get("email"):
    email = input("Email manzilingiz? ")
    xotira["shaxsiy_malumotlar"]["email"] = email
    xotirani_saqlash(xotira)
    print("RAV AI: Email manzilingiz saqlandi! ")

print(" Bugungi vazifalaringiz:")

if xotira["vazifalar"]:
    for i, vazifa in enumerate(xotira["vazifalar"], 1):
        print(f"   {i}. {vazifa}")
else:
    print("   Hozircha vazifa yo`q.")

yangi = input("Yangi vazifa qo'shish? (ha/yo`q): ").lower().strip()
if yangi in ["ha", "h", "yes"]:
    vazifa = input("Vazifani kiriting: ")
    xotira["vazifalar"].append(vazifa)
    xotirani_saqlash(xotira)
    print(f"RAV AI: '{vazifa}' vazifasi qo'shildi! ✅")

print("\n💬 RAV AI Chatbot (chiqish uchun 'xayr' yozing)")

# =====================
# CHATBOT
# =====================
print("💬 RAV AI Chatbot (chiqish uchun 'xayr' yozing)")

print("-" * 40)

while True:
    savol = input("Siz: ").lower().strip()

    if not savol:
     continue
    # Chiqish
    if savol in ["xayr", "bye", "quit", "chiqish"]:
        print("RAV AI: Xayr! Yana murojaat qiling! 👋")
        break

    # Salomlashish
    elif "salom" in savol or "hello" in savol or "hi" in savol:
        print(f"RAV AI: Salom, {xotira['shaxsiy_malumotlar']['ism']}! 👋")

    # Yordam
    elif "yordam" in savol or "help" in savol or "pomosh" in savol:
        print("RAV AI: Albatta yordam beraman! 💪 Quyidagilarni so'rashingiz mumkin:")
        print("   • 'salom' — salomlashish")
        print("   • 'vazifa' — vazifalarni ko'rish")
        print("   • 'yangi vazifa' — vazifa qo'shish")
        print("   • 'vaqt' — hozirgi vaqt")
        print("   • 'bugun' — bugungi sana")
        print("   • 'yosh' — yoshingiz")
        print("   • 'xayr' — chiqish")

    # Ism ← "yordam" so'zi yo'qligini tekshiramiz!
    elif ("ism" in savol or "nomi" in savol) and "yordam" not in savol:
        print("RAV AI: Mening nomim RAV AI! 🤖")

    # Yosh
    elif "yosh" in savol:
        print(f"RAV AI: Siz {xotira['shaxsiy_malumotlar'].get('yosh', '?')} yoshdasiz!")

    # Vazifalar
    elif "vazifa" in savol:
        vazifalar = xotira["vazifalar"]
        if vazifalar:
            print("RAV AI: Sizning vazifalaringiz:")
            for i, v in enumerate(vazifalar, 1):
                print(f"   {i}. {v}")
        else:
            print("RAV AI: Hozircha vazifa yo`q!")

    # Yangi vazifa
    elif "yangi vazifa" in savol:
        v = input("Vazifani kiriting: ")
        xotira["vazifalar"].append(v)
        xotirani_saqlash(xotira)
        print(f"RAV AI: '{v}' vazifasi qo'shildi! ✅")

    # Qanday
    elif "qanday" in savol or "yaxshimisan" in savol or "qalaysan" in savol:
        print("RAV AI: Yaxshiman, rahmat! Siz-chi? 😊")

    # Rahmat
    elif "rahmat" in savol:
        print("RAV AI: Arzimaydi! 😊")

    # Vaqt
    elif "vaqt" in savol or "soat" in savol:
        import datetime
        hozir = datetime.datetime.now().strftime("%H:%M")
        print(f"RAV AI: Hozir soat {hozir}! ⏰")

    # Kun
    elif "bugun" in savol or "kun" in savol:
        import datetime
        bugun = datetime.datetime.now().strftime("%d-%m-%Y")
        print(f"RAV AI: Bugun {bugun}! 📅")

    # Inglizcha
    elif "what" in savol or "who" in savol or "how" in savol:
        print("RAV AI: I am RAV AI — your personal assistant! 🤖")

    # Ruscha
    elif "привет" in savol or "как" in savol:
        print("RAV AI: Привет! Я RAV AI — ваш личный помощник! 🤖")

    # Noma'lum savol
    else:
        print("RAV AI: Hali bu savolni o'rganmadim, lekin o'rganaman! 🧠")

    # Suhbatni saqlash
    xotira["suhbat_tarixi"].append({"savol": savol,"vaqt": __import__("datetime").datetime.now().strftime("%H:%M")})
        
    xotirani_saqlash(xotira)  
print("Xotiradagi ma'lumotlar:")
print(xotira["shaxsiy_malumotlar"])