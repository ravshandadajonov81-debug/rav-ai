import io

with io.open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

q = chr(34)
old_line = "return {'+chr(34)+'javob'+chr(34)+': javobni_tarjima_qil('+chr(34)+'Iltimos shahar nomini aniqroq korsating.'+chr(34)+', data.matn)}"
new_line = "return {" + q + "javob" + q + ": javobni_tarjima_qil(" + q + "Iltimos shahar nomini aniqroq korsating." + q + ", data.matn)}"

old_line2 = "return {'+chr(34)+'javob'+chr(34)+': natija}"
new_line2 = "return {" + q + "javob" + q + ": natija}"

old_line3 = "return {'+chr(34)+'javob'+chr(34)+': javobni_tarjima_qil(eski_natija, data.matn)}"
new_line3 = "return {" + q + "javob" + q + ": javobni_tarjima_qil(eski_natija, data.matn)}"

count = 0
if old_line in content:
    content = content.replace(old_line, new_line, 1)
    count += 1
if old_line2 in content:
    content = content.replace(old_line2, new_line2, 1)
    count += 1
if old_line3 in content:
    content = content.replace(old_line3, new_line3, 1)
    count += 1

with io.open("server.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Tuzatildi! " + str(count) + " ta qator almashtirildi.")