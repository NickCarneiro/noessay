import base64

secret_key = long(0xD89E452B820C4875)
chaff = 656538804247

def is_empty(str):
    if str is None:
        return True
    elif str == '':
        return True
    else:
        return False
# decrypt scholarship key (outputs scholarship id)
def decrypt_sk(sk):
    sk_long = long(sk)
    sid = sk_long ^ secret_key
    sid_dechaffed = sid / chaff
    return sid_dechaffed

#encrypt scholarship id (outputs scholarship key)
def encrypt_sid(sid):
    encrypted_sid = (sid * chaff) ^ secret_key
    return str(encrypted_sid)