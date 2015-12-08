# -*- coding: utf-8 -*-
import socket  
import configparser
import datetime
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Cipher import ARC4
import hashlib
import base64
from Crypto import Random

config = configparser.ConfigParser()
config.read("configServer.cfg")  

outfile = open('confidencial.txt', 'w')
    
size = int(config.get("S1", "blockSize"))
padding = config.get("S1","padding")*16
    
pad = lambda s: s + (size - len(s) % size) * padding
    
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode("ISO-8859-1").rstrip(padding)
    

def servidor():
        
    IV = 16 * '\x00'
    password = config.get("S1", "keyServer").encode(encoding='utf_8')
    key = hashlib.sha256(password).digest()
    
    opciones = {
        1 : 'AES',
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
    
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Enlace de socket y puerto
    server_address = (config.get("S1", "ip"), int(config.get("S1", "puerto")))
    print ( 'Empezando a levantar ' + server_address[0] + ' puerto ' + str(server_address[1]))
    sock.bind(server_address)
    
    # Escuchando conexiones entrantes
    sock.listen(1)
     
    recibidos = []
        
    while True:
        # Esperando conexion
        print ('Esperando para conectarse\n')
        connection, client_address = sock.accept()
        
        try:
            print ('conexion desde ' + client_address[0])
     
            # Recibe los datos en trozos y reetransmite
            while True:
                data = connection.recv(1024)
                data = DecodeAES(cipher, data)
                recibidos.append(data)
                
                print ('recibido..\n' + data)
                        
                notifi = "OK"
                
                data = str(data).replace(",", "")
                data = str(data).replace(" ", "")
                
                if (data.isdigit() == False):
                    
                    outfile = open('confidencial.txt', 'a')
                    notifi = "ERROR - No se pudo descifrar el mensaje"
                    out = str(datetime.datetime.now()) + " - " + str(data) + " - " + notifi + " \n"
                    outfile.write(out)
                    outfile.close()
                
                if data:
                    
                    print ('Enviando mensaje de vuelta al cliente')
                    encoded = EncodeAES(cipher, notifi)
                    print ('Encrypted string:', encoded)
                    connection.sendall(encoded)
                 
            
                else:
                    print ('No hay mas datos de ' + client_address[0])
            
                    break
                
                break
            
        except EOFError: 
            ret = []
      
        finally:
            # Cerrando conexion
            
            connection.close()
    del encoded
    del data
    del cipher
            
            
if __name__ == '__main__':
    
    servidor()
