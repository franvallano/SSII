from Crypto.PublicKey import RSA
import os
import time
from Crypto.Hash import SHA256
import base64

def hashed(message):
    
    h = SHA256.new()
    h.update(message)
    return h.hexdigest()

def compare_hash(h1,h2):
    
    c = "OK"
    if (h1 != h2):
        c = "ERROR"
    print(c)

def generate_RSA(bits):
    
    new_key = RSA.generate(bits, e=65537)
    pub = open("public_key.der","w")
    pri = open("private_key.der","w")
    public_key = new_key.publickey().exportKey("DER")
    pub.write(str(public_key)) 
    private_key = new_key.exportKey("DER")
    pri.write(str(private_key))
    pub.close()
    pri.close()
    return private_key, public_key



def encrypt_file( file, public):
    
    tami = os.path.getsize(file)
    print( "Tamaño inicial: " + str(tami) )
    inicio = time.time()*1000
    with open(file, 'rb') as fo:
        file_to_encrypt = fo.read()
    fo.close()
    h = hashed(file_to_encrypt)
    o = RSA.importKey(public)
    to_join = []
    step = 0
    
    while 1:
        # Read 128 characters at a time.
        s = file_to_encrypt[step*128:(step+1)*128]
        if not s: 
            break
        # Encrypt with RSA and append the result to list.
        # RSA encryption returns a tuple containing 1 string, so i fetch the string.
        to_join.append(o.encrypt(s, 0)[0])
        step += 1
    
    encrypted = b''.join(to_join)
    name = file.replace(".","")
    nam = name + ".enc"
    with open(nam, 'wb') as fo:
        fo.write(encrypted)
    fo.close()
    fin = time.time()*1000
    tamf = os.path.getsize(nam)
    tiempo_total = fin - inicio
    print("Codigo Hash: " + str(h))
    print( "Tiempo de ejecucion : " + str(tiempo_total) )
    print( "Tamaño final : " + str(tamf) + "\n")
    return h



def decrypt_file( file, private):
    
    tami = os.path.getsize(file)
    print( "Tamaño inicial: " + str(tami) )
    inicio = time.time()*1000
    with open(file, 'rb') as fo:
        file_to_decrypt = fo.read()
    fo.close()
    o = RSA.importKey(private)
    to_join = []
    step = 0
    
    while 1:
        # Read 128 characters at a time.
        s = file_to_decrypt[step*128:(step+1)*128]
        if not s: 
            break
        # Encrypt with RSA and append the result to list.
        # RSA encryption returns a tuple containing 1 string, so i fetch the string.
        to_join.append(o.decrypt(s))
        step += 1
    
    decrypted = b''.join(to_join)
    name = file.replace(".","")
    nam = name[:-4] + ".txt"
    with open(nam, 'wb') as fo:
        fo.write(decrypted)
    fo.close()
    with open(nam, 'rb') as fo:
        text = fo.read()
    fo.close()
    h = hashed(text)
    fin = time.time()*1000
    tamf = os.path.getsize(nam)
    tiempo_total = fin - inicio
    print("Codigo Hash: " + str(h))
    print( "Tiempo de ejecucion : " + str(tiempo_total) )
    print( "Tamaño final : " + str(tamf) )
    return h



if __name__ == '__main__':
    
    g = generate_RSA(2048)
   
    print("\nArchivo de 10Kb")
    e = encrypt_file('10KB.txt', g[1])
    d = decrypt_file('10KBtxt.enc', g[0])
    compare_hash(e, d)
    
    print("\nArchivo de 1Mb")
    e1 = encrypt_file('1MB.txt', g[1])
    d1 = decrypt_file('1MBtxt.enc', g[0])
    compare_hash(e1, d1)
    
    print("\nArchivo de 10Mb")
    e2 = encrypt_file('10MB.txt',g[1] )
    d2 = decrypt_file('10MBtxt.enc', g[0])
    compare_hash(e2, d2)
    
    print("\nArchivo de 20Mb")
    e3 = encrypt_file('20MB.txt', g[1])
    d3 = decrypt_file('20MBtxt.enc', g[0])
    compare_hash(e3, d3)
    
    
    
    
