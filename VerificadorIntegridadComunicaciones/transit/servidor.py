# -*- coding: utf-8 -*-
import socket  
import configparser
import pickle
import hmac
import datetime

config = configparser.ConfigParser()
config.read("config.cfg")  

outfile = open('integridad.txt', 'w')

opciones = {
    1 : 'md5',
    2 : 'sha1',
    3 : 'sha256'
}

algoritmo = config.get("S1", "Hash")


if algoritmo == opciones.get(1): 
    cod = 'md5'
    tam = 32
elif algoritmo == opciones.get(2):
    cod = 'sha1'
    tam = 40
else:
    cod = 'sha256'
    tam = 64

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
    outfile = open('integridad.txt', 'a')
    
    try:
        print ('conexion desde ' + client_address[0])
 
        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(1024)
            d = pickle.loads(data)
            
            recibidos.append(d)
            
            print ('recibido..\n ' + str(d))
            
            keyword = config.get("S1", "key").encode('utf-8')
            mensaje = d[0].encode('utf-8') 
            code = d[1].encode('utf-8') 
            
            hashing = code[0:tam].decode('utf-8')
            
            tamCod = len(code) 
            
            time = code[tam+1:tamCod].decode('utf-8')
            
            digest_maker = hmac.new( keyword, mensaje , cod)
            
            digest_maker.update(mensaje)
            
            digest = digest_maker.hexdigest()
                    
            notifi = "OK"
            
            if (digest != hashing and time in recibidos):
                
                notifi = "ERROR - Integridad violada"
                out = str(datetime.datetime.now()) + " - " + str(d) + " - " + notifi + " \n"
                outfile.write(out)
            
            if data:
                print ('Enviando mensaje de vuelta al cliente')
                d.append(notifi)
                connection.sendall(pickle.dumps(d))
        
            else:
                print ('No hay mas datos de ' + client_address[0])
                
                del digest_maker 
                
                break
            
            
    except EOFError: 
        ret = []
  
    finally:
        # Cerrando conexion
        connection.close()
        outfile.close()
