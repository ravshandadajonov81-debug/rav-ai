f = open("server.py", "r", encoding="utf-8")
lines = f.readlines()
f.close()

result = []
for line in lines:
    if 'kalit_sozlar = ["hozir", "bugun", "ob-havo", "ob havo", "weather", "harorat", "iqlim"]' in line:
        line = line.replace(
            '["hozir", "bugun", "ob-havo", "ob havo", "weather", "harorat", "iqlim"]',
            '["hozir", "bugun", "ob-havo", "ob havo", "weather", "harorat", "iqlim", "havo"]'
        )
    result.append(line)

f = open("server.py", "w", encoding="utf-8")
f.writelines(result)
f.close()
print("OK!")