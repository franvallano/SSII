# -*- coding: utf-8 -*-
import socket
from tkinter import *
import pickle
import ssl
import pprint

def cliente():
    
    
    def insertar():
        
        u = e1.get()
        p = e2.get()
                
        msg = [u, p]
            
        print ('enviando..\n ' +  str(msg))
                    
        ssl_sock.sendall(pickle.dumps(msg))
        
        root.destroy()
        
        return msg
        
        
    def cancelarPanel():
        
        root.destroy()
        
    # Creando un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ssl_sock = ssl.wrap_socket(sock, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED, ssl_version = ssl.PROTOCOL_TLSv1)
    
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 4444)
    
    print ('conectando a ' + server_address[0] + ' y puerto ' + str(server_address[1]))
    
    ssl_sock.connect(server_address)
    
    #Muestra informacion de certificado
    #print (repr(ssl_sock.getpeername()))
    #print (ssl_sock.cipher())
    #print (pprint.pformat(ssl_sock.getpeercert()))
        
    try:
        
        root = Tk()
        
        username = Label(root , text = "Username")
        e1 = Entry(root , bd = 10)
            
        password = Label(root , text = "Password")
        e2 = Entry(root , bd = 10)
            
        aceptar = Button (root , text = "Aceptar", command = insertar)
        cancelar = Button (root , text = "Cancelar", command = cancelarPanel )
            
        username.pack()
        e1.pack()
        password.pack()
        e2.pack()
        aceptar.pack(side = LEFT)
        cancelar.pack(side = RIGHT)
            
        root.mainloop()
    
        while True:
            
            data = ssl_sock.recv(1024).decode("utf_8")
            
            if (data):
                
                print ( 'recibiendo..\n' + str(data))
           
                root = Tk()
                        
                msg = Label(root , text = str(data))
                acept = Button (text = "Aceptar" , command = cancelarPanel)        
                
                msg.pack()
                acept.pack()
                        
                root.mainloop()
                
                break
            
            break
        
    finally:
        print ('cerrando socket\n\n')
        ssl_sock.close()
    
if __name__ == '__main__':
    
    cliente()