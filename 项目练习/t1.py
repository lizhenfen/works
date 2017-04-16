from passlib.hash import  sha512_crypt


en_data1 = sha512_crypt.encrypt("data")
en_data2 = sha512_crypt.hash("data")

print(en_data1)
print(en_data2)
