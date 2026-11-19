import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

eski = '''def deep_tarjima_qil(matn, til_kodi):
    try:
        if til_kodi and til_kodi.lower() in ("uz", "uz-uz"):
            return matn
        from deep_translator import MyMemoryTranslator
        import html
        kod = mymemory_til_kodi_topish(til_kodi)
        natija = MyMemoryTranslator(source="en-GB", target=kod).translate(matn)
        if natija:
            natija = html.unescape(natija)
        return natija
    except Exception as e:
        print("Deep-translator xatosi:", e)
        return None'''

yangi = '''def deep_tarjima_qil(matn, til_kodi):
    try:
        if til_kodi and til_kodi.lower() in ("uz", "uz-uz"):
            return matn
        from deep_translator import MyMemoryTranslator
        import html, re
        himoya_belgisi = "XSOMX9Y"
        matn_himoyalangan = re.sub(r"\\bsom\\b", himoya_belgisi, matn, flags=re.IGNORECASE)
        kod = mymemory_til_kodi_topish(til_kodi)
        natija = MyMemoryTranslator(source="en-GB", target=kod).translate(matn_himoyalangan)
        if natija:
            natija = html.unescape(natija)
            natija = natija.replace(himoya_belgisi, "som").replace(himoya_belgisi.lower(), "som").replace(himoya_belgisi.capitalize(), "Som")
        return natija
    except Exception as e:
        print("Deep-translator xatosi:", e)
        return None'''

if eski in content:
    content = content.replace(eski, yangi)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")