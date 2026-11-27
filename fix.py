with open('server.py', 'r', encoding='utf-8') as f:
    qatorlar = f.readlines()

qatorlar[812] = '    import re\n    natija = matn\n'

with open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(qatorlar)

print("Tayyor!")