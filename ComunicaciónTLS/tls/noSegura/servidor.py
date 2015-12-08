# -*- coding: utf-8 -*-
import socket  
import datetime
from tkinter import *
import pickle


USERNAME = "fran"
PASSWORD = "fran"


def servidor():
      
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Enlace de socket y puerto
    server_address = ('localhost', 4444)
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
                
                d = pickle.loads(data)
                
                recibidos.append(d)
                
                #QUITAR
                print ('recibido..\n' + str(d))
                
                username = str(d[0]) 
                password = str(d[1])
                
                notifi = ""
                
                if (USERNAME == username and PASSWORD == password):
                
                    notifi =  "Wellcome, " + username
        
                else:
                    
                    outfile = open('error.txt', 'a')
                    notifi = "ERROR - Usuario y/o contraseña no son correctos"
                    out = str(datetime.datetime.now()) + " - " + str(d) + " - " + notifi + " \n"
                    outfile.write(out)
                    outfile.close()
                    
                
                if data:
                    
                    print ('Enviando mensaje de vuelta al cliente')
                    connection.sendall(notifi.encode('utf_8'))
                    print(notifi)
            
                else:
                    print ('No hay mas datos de ' + client_address[0])
            
                    break
                
                break
            
        except EOFError: 
            ret = []
      
        finally:
            # Cerrando conexion
            
            connection.close()
            
            
if __name__ == '__main__':
    
    servidor()
