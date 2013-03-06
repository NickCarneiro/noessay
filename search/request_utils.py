import re
from pyDes import *
import base64
secret_key = 'Fitzgeralds remarks abou'
crypt = triple_des(secret_key, mode=ECB, padmode=PAD_PKCS5)

def is_empty(str):
    if str is None:
        return True
    elif str == '':
        return True
    else:
        return False

def int_to_bytes(data):
    assert isinstance(data, int), 'input was not an int'
    byte_array = []
    for s in 24,16,8,0:
        byte_array.append(((data >> s) & 0xff))
    return byte_array

def bytes_to_int(data):
    assert len(data) == 4, 'must pass in a str/collection of 4 elements'
    return (
        (ord(data[0]) & 0xff) << 24 |
        (ord(data[1]) & 0xff) << 16 |
        (ord(data[2]) & 0xff) << 8 |
        (ord(data[3]) & 0xff)
        )
# decrypt scholarship key (outputs scholarship id)
def decrypt_sk(sk):

    assert isinstance(sk, basestring) and len(sk) == 16, (
        'scholarship key was not a valid string')
    encrypted_byte_array = []
    for i in re.findall('..', sk):
        encrypted_byte_array.append(chr(int(i,16)))
    bytes = ''.join(encrypted_byte_array)
    return str(bytes_to_int( crypt.decrypt(bytes) ))

#encrypt scholarship id (outputs scholarship key)
def encrypt_sid(sid):
    assert isinstance(sid, basestring), 'scholarship id was not a string'
    sid_chars = []
    for ch in int_to_bytes(int(sid)):
        sid_chars.append(chr(ch))
    sid_enc = crypt.encrypt(sid_chars)
    return ''.join("{:02x}".format(ord(c)) for c in sid_enc)

def test_encryption():
    x = str(1234567890)
    print x
    y = encrypt_sid(x)
    print y
    print decrypt_sk(y)

#test_encryption()
def parse_string_param(param, default):
    if param is None or param == '':
        return default
    else:
        return param

def parse_int_param(param, default):
    try:
        parsed = int(param)
    except TypeError:
        parsed = default
    except ValueError:
        parsed = default
    return parsed

def parse_boolean_param(param):
    parsed = param == 'true' or param == 'True' or param == '1'
    return parsed



