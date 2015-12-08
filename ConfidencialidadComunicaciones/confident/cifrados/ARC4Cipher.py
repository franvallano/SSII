from Crypto.Cipher import ARC4
import time
import os

def pad(s):
    
    return s + b"\0" * (ARC4.block_size - len(s) % ARC4.block_size)

def encrypt(message, key, key_size=256):
    
    message = pad(message)
    cipher = ARC4.new(key)
    return cipher.encrypt(message)

def decrypt(ciphertext, key):
    
    cipher = ARC4.new(key)
    plaintext = cipher.decrypt(ciphertext[ARC4.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    tami = os.path.getsize(file_name)
    print( "Tamaño inicial : " + str(tami) )
    inicio = time.time()*1000
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    fo.close()
    enc = encrypt(plaintext, key)
    name = file_name.replace(".","")
    with open(name + ".enc", 'wb') as fo:
        fo.write(enc)
    fo.close()
    fin = time.time()*1000    
    outfile = name + ".enc"
    tamf = os.path.getsize(outfile)
    tiempo_total = fin - inicio
    print( "Tiempo de ejecucion : " + str(tiempo_total) )
    print( "Tamaño final : " + str(tamf) + "\n")

def decrypt_file(file_name, key):
    inicio = time.time()*1000
    tami = os.path.getsize(file_name)
    print( "Tamaño inicial : " + str(tami) )
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    fo.close()
    dec = decrypt(ciphertext, key)
    name = file_name[:-4] + ".txt"
    with open(name, 'wb') as fo:
        fo.write(dec)
    fo.close()
    fin = time.time()*1000   
    tamf = os.path.getsize(name)
    tiempo_total = fin - inicio
    print( "Tiempo de ejecucion : " + str(tiempo_total) )
    print( "Tamaño final : " + str(tamf) )



key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'


if __name__ == '__main__':
    
    print("Archivo de 10Mb")
    encrypt_file('10MB.txt', key)
    decrypt_file('10MBtxt.enc', key)
    
    print("\nArchivo de 1Mb")
    encrypt_file('1MB.txt', key)
    decrypt_file('1MBtxt.enc', key)
    
    print("\nArchivo de 20Mb")
    encrypt_file('20MB.txt', key)
    decrypt_file('20MBtxt.enc', key)
    
    print("\nArchivo de 10Kb")
    encrypt_file('10KB.txt', key)
    decrypt_file('10KBtxt.enc', key)