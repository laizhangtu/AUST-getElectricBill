import base64
import random
from Crypto.Cipher import AES

AES_CHARS = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'

def random_string(length):
    return ''.join(random.choice(AES_CHARS) for _ in range(length))

def pkcs7_pad(data):
    bs = AES.block_size  # 16
    padding = bs - (len(data.encode('utf-8')) % bs)
    return data + chr(padding) * padding

def pkcs7_unpad(data):
    padding = ord(data[-1])
    return data[:-padding]

def get_aes_string(data, key0, iv0):
    key0 = key0.strip()
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    padded_data = pkcs7_pad(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(padded_data.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def encrypt_aes(data, aes_key):
    if not aes_key:
        return data
    return get_aes_string(random_string(64) + data, aes_key, random_string(16))

def encrypt_password(pwd0, key):
    try:
        return encrypt_aes(pwd0, key)
    except Exception:
        return pwd0

def decrypt_password(data, aes_key):
    try:
        key = aes_key.encode('utf-8')
        iv = random_string(16).encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_bytes = cipher.decrypt(base64.b64decode(data))
        decrypted_str = pkcs7_unpad(decrypted_bytes.decode('utf-8'))
        return decrypted_str[64:]
    except Exception:
        return data
