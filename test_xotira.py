import server

server.foydalanuvchini_saqla("12345", ism="Ravshan", shahar="Shirin", mavzu="ob-havo")
server.foydalanuvchini_saqla("12345", shahar="Shirin", mavzu="ob-havo")
server.foydalanuvchini_saqla("12345", shahar="Toshkent")

foydalanuvchi = server.foydalanuvchini_olish("12345")
print("Foydalanuvchi:", foydalanuvchi)

sevimli = server.sevimli_shahar_olish("12345")
print("Sevimli shahar:", sevimli)