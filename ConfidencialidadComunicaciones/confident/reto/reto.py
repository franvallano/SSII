from Crypto.Cipher import AES
import Crypto.Random
from PIL import Image
import base64


def mostrarImagen(imagen):
    
    im = Image.open(imagen)
    im.show()
      
def pad(s):
    
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    
    message = pad(message)
    iv = Crypto.Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB, iv)
    return iv + cipher.encrypt(message)

def encrypt_file(file_name, key):
    
    with open(file_name, 'rb') as fo:
        plaintext = base64.b64encode(fo.read())
    fo.close()
    enc = encrypt(plaintext, key)
    name = file_name.replace(".","")
    with open(name + ".bmp", 'wb') as fo:
        fo.write(enc)
    fo.close()


key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

if __name__ == "__main__":
   
    encrypt_file("us.bmp",key)


    