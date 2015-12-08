from Crypto import Random
from Crypto.Cipher import DES3
import time
import os
from Crypto.Hash import SHA256

def pad(s):
    
    return s + b"\0" * (DES3.block_size - len(s) % DES3.block_size)

def encrypt(message, key, key_size=256):
    
    message = pad(message)
    iv = Random.new().read(8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    
    iv = Random.new().read(8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[DES3.block_size:])
    return plaintext.rstrip(b"\0")

def hashed(message):
    
    h = SHA256.new()
    h.update(message)
    return h.hexdigest()

def compare_hash(h1,h2):
    
    c = "OK"
    if (h1 != h2):
        c = "ERROR"
    print(c)

def encrypt_file(file_name, key):
    tami = os.path.getsize(file_name)
    print( "Tamaño inicial : " + str(tami) )
    inicio = time.time()*1000
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    fo.close()
    h = hashed(plaintext)
    enc = encrypt(plaintext, key)
    name = file_name.replace(".","")
    with open(name + ".enc", 'wb') as fo:
        fo.write(enc)
    fo.close()
    fin = time.time()*1000   
    outfile = name + ".enc"
    tamf = os.path.getsize(outfile)
    tiempo_total = fin - inicio
    print("Codigo Hash: " + str(h))
    print( "Tiempo de ejecucion : " + str(tiempo_total) )
    print( "Tamaño final : " + str(tamf) + "\n")
    return h

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
    with open(name, 'rb') as fo:
        text = fo.read()
    fo.close()
    h = hashed(text)
    fin = time.time()*1000   
    tamf = os.path.getsize(name)
    tiempo_total = fin - inicio
    print("Codigo Hash: " + str(h))
    print( "Tiempo de ejecucion : " + str(tiempo_total) )
    print( "Tamaño final : " + str(tamf) )
    return h


#key must be either 16 or 24 bytes long
key = b'-8B key--8B key-'

if __name__ == '__main__':
    
    print("Archivo de 10Mb")
    e = encrypt_file('10MB.txt', key)
    d = decrypt_file('10MBtxt.enc', key)
    compare_hash(e, d)
    
    print("\nArchivo de 1Mb")
    e1 = encrypt_file('1MB.txt', key)
    d1 = decrypt_file('1MBtxt.enc', key)
    compare_hash(e1, d1)
    
    print("\nArchivo de 20Mb")
    e2 = encrypt_file('20MB.txt', key)
    d2 = decrypt_file('20MBtxt.enc', key)
    compare_hash(e2, d2)
    
    print("\nArchivo de 10Kb")
    e3 = encrypt_file('10KB.txt', key)
    d3 = decrypt_file('10KBtxt.enc', key)
    compare_hash(e3, d3)