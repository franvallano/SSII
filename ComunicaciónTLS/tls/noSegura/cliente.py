# -*- coding: utf-8 -*-
import socket
from tkinter import *
import pickle


def cliente():
    
    
    def insertar():
        
        u = e1.get()
        p = e2.get()
                
        msg = [u, p]
            
        print ('enviando..\n ' +  str(msg))
                    
        sock.sendall(pickle.dumps(msg))
        
        root.destroy()
        
        return msg
        
        
    def cancelarPanel():
        
        root.destroy()
        
    # Creando un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 4444)
    
    print ('conectando a ' + server_address[0] + ' y puerto ' + str(server_address[1]))
    
    sock.connect(server_address)
    
        
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
            
            data = sock.recv(1024).decode("utf_8")
            
            if (data):
                
            #amount_received += len(data)
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
        sock.close()
    
if __name__ == '__main__':
    
    cliente()