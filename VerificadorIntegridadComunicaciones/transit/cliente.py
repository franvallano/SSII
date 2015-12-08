# -*- coding: utf-8 -*-
import socket
import configparser
import hmac
import pickle
import datetime

config = configparser.ConfigParser()
config.read("config.cfg")

time = str(datetime.datetime.now())
time = time.replace(" ","")
time = time.replace("-","")
time = time.replace(":","")
time = time.replace(".","")


opciones = {
    1 : 'md5',
    2 : 'sha1',
    3 : 'sha256'
}

algoritmo = config.get("S1", "Hash")


if algoritmo == opciones.get(1): 
    cod = 'md5'
elif algoritmo == opciones.get(2):
    cod = 'sha1'
else:
    cod = 'sha256'

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
    
    keyword = config.get("S1", "key").encode('utf-8')
    mensaje = message.encode('utf-8') 
    
    
    digest_maker = hmac.new( keyword, mensaje , cod)
    
    digest_maker.update(mensaje)
    
    digest = digest_maker.hexdigest() + str(time)
    
    msgs = [message,digest]
    
    sock.sendall(pickle.dumps(msgs))
 
    # Buscando respuesta
    amount_received = 0
    amount_expected = len(message)
     
    while amount_received < amount_expected:
        data = sock.recv(1024)
        d = pickle.loads(data)
        amount_received += len(data)
        print ( 'recibiendo..\n' + str(d))
    
    
    del digest_maker
   
finally:
    print ('cerrando socket\n\n')
    sock.close()