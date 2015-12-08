# -*- coding: utf-8 -*-
import socket
import configparser
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Cipher import ARC4
import hashlib
import base64
from Crypto import Random

config = configparser.ConfigParser()
config.read("configCliente.cfg")
    
size = int(config.get("S1", "blockSize"))
padding = config.get("S1","padding")*16
    
pad = lambda s: s + (size - len(s) % size) * padding
    
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode("ISO-8859-1").rstrip(padding)



def cliente():
    
    IV = 16 * '\x00'
    password = config.get("S1", "keyClient").encode(encoding='utf_8')
    key = hashlib.sha256(password).digest()
    
    opciones = {
        1: 'AES',
        2 : 'Blowfish',
        3 : 'ARC4'
    }
    
    op_mode = {
        1 : "CBC",       
        2 : "ECB",
        3 : "CFB"           
    }
    
    cip = config.get("S1", "cipher")
    mode = config.get("S1", "mode")
    
    if cip == opciones.get(1):
        
        if mode == op_mode.get(1):
            m = AES.MODE_CBC
        elif mode == op_mode.get(2):
            m = AES.MODE_ECB
        else:
            m = AES.MODE_CFB
        
        cipher = AES.new(key,m,IV)
    
    elif cip == opciones.get(2):
        
        if mode == op_mode.get(1):
            m = Blowfish.MODE_CBC
        elif mode == op_mode.get(2):
            m = Blowfish.MODE_ECB
        else:
            m = Blowfish.MODE_CFB
            
        IV = 8 * "\x00"
        cipher = Blowfish.new(key, m ,IV)
        
    elif cip == opciones.get(3):
        cipher = ARC4.new(key)
    
    # Creando un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = (config.get("S1", "ip"), int(config.get("S1", "puerto")))
    
    print ('conectando a ' + server_address[0] + ' y puerto ' + str(server_address[1]))
    
    sock.connect(server_address)
    
    try:
        
        # Enviando datos
        message = config.get("S1", "cuentaOrigen") + "," + config.get("S1", "cuentaDestino") + "," + config.get("S1", "cantidad")     
        print ('enviando..\n ' +  message)
        
        print(len(message))
        
        encoded = EncodeAES(cipher, message)
        print ('Encrypted string:', encoded)
        
        sock.sendall(encoded)
     
        # Buscando respuesta
        amount_received = 0
        amount_expected = len(message)
         
        while amount_received < amount_expected:
            data = sock.recv(1024)
            decoded = DecodeAES(cipher, data)
            amount_received += len(data)
            print ( 'recibiendo..\n' + str(decoded))
       
    finally:
        print ('cerrando socket\n\n')
        sock.close()
    del cipher
        
        
if __name__ == '__main__':
    
    cliente()