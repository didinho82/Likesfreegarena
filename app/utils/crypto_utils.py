import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Chaves Reais extraídas do jogo
MAIN_KEY = b'6D59713374367739'
MAIN_IV = b'3333333333333333'

def encrypt(data):
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt(data):
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    return unpad(cipher.decrypt(data), AES.block_size)
