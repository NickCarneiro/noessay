from pyDes import *
import base64
key = 'redevelo'
k = des(key, CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)

def is_empty(str):
    if str is None:
        return True
    elif str == '':
        return True
    else:
        return False

# decrypt scholarship key (outputs scholarship id)
def decrypt_sk(sk):
    hex_upper = sk.upper()
    bytes = base64.b16decode(hex_upper)
    dec_hex = str(k.decrypt(bytes))
    dec = long(dec_hex, 16)
    return dec

#encrypt scholarship id (outputs scholarship key)
def encrypt_sid(sid):
    sid_hex = hex(sid).replace('0x', '')
    enc = k.encrypt(str(sid_hex))
    encrypted_hex = base64.b16encode(enc)
    return encrypted_hex.lower()

def test_encryption():
    x = 234567890
    print x
    y = encrypt_sid(x)
    print y
    print decrypt_sk(y)

#test_encryption()