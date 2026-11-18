import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

boshi_marker = "OB_HAVO_LABELLAR = "
oxiri_marker = "def deep_tarjima_qil(matn, til_kodi):"

boshi = content.find(boshi_marker)
oxiri = content.find(oxiri_marker)

if boshi == -1 or oxiri == -1 or boshi > oxiri:
    print("Markerlar topilmadi, boshi=", boshi, "oxiri=", oxiri)
else:
    yangi_blok = '''OB_HAVO_LABELLAR = ["Harorat:", "his:", "Namlik:", "Shamol:", "Holat:", "3 kunlik:", "Bugun:", "Ertaga:", "Indinga:"]

def ob_havo_tarjima_qil(matn, til_kodi):
    try:
        tarjima_kesh = {}
        natija = matn
        for label in OB_HAVO_LABELLAR:
            if label in natija:
                if label not in tarjima_kesh:
                    t = deep_tarjima_qil(label, til_kodi)
                    tarjima_kesh[label] = t if t else label
                natija = natija.replace(label, tarjima_kesh[label])
        return natija
    except Exception as e:
        print("Ob-havo tarjima xatosi:", e)
        return None

def ob_havo_toliq_tarjima_qil(matn, til_kodi):
    try:
        natija = deep_tarjima_qil(matn, til_kodi)
        if not natija:
            return matn
        qolgan_ozbekcha = ["Bugun:", "Ertaga:", "Indinga:", "kunlik"]
        if any(s in natija for s in qolgan_ozbekcha):
            natija = ob_havo_tarjima_qil(natija, til_kodi)
        return natija
    except Exception as e:
        print("Ob-havo toliq tarjima xatosi:", e)
        return matn

'''
    content = content[:boshi] + yangi_blok + content[oxiri:]
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")