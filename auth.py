import json
import os
import hashlib

USERS_FAYILI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def parol_hash(parol):
    return hashlib.sha256(parol.encode()).hexdigest()

def users_yuklash():
    if os.path.exists(USERS_FAYILI):
        with open(USERS_FAYILI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def users_saqlash(users):
    with open(USERS_FAYILI, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def royxatdan_otish(username, parol, ism):
    users = users_yuklash()
    if username in users:
        return False, "Bu foydalanuvchi allaqachon mavjud!"
    users[username] = {
        "ism": ism,
        "parol_hash": parol_hash(parol),
        "xotira": {
            "shaxsiy_malumotlar": {"ism": ism},
            "vazifalar": [],
            "suhbat_tarixi": []
        }
    }
    users_saqlash(users)
    return True, "Muvaffaqiyatli royxatdan otdingiz!"

def kirish(username, parol):
    users = users_yuklash()
    if username not in users:
        return False, "Foydalanuvchi topilmadi!"
    if users[username]["parol_hash"] != parol_hash(parol):
        return False, "Parol notogri!"
    return True, users[username]

def xotira_saqlash(username, xotira):
    users = users_yuklash()
    if username in users:
        users[username]["xotira"] = xotira
        users_saqlash(users)