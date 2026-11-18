import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

eski = '''            MYMEMORY_TILLAR_KESH = MyMemoryTranslator().get_supported_languages(as_dict=True)'''

yangi = '''            MYMEMORY_TILLAR_KESH = MyMemoryTranslator(source="en-GB", target="en-GB").get_supported_languages(as_dict=True)'''

if eski in content:
    content = content.replace(eski, yangi)
    with io.open("server.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tuzatildi!")
else:
    print("Topilmadi")