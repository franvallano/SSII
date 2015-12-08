__author__ = "Fco. Javier Delgado Vallano"
__copyright__ = "Copyright (C) 2005 Fco. Javier Delgado Vallano"

# -*- coding: utf-8 -*-
import configparser
import hashlib
import sqlite3
import os
from smtplib import SMTP
from email.mime.text import MIMEText
import time


  
config = configparser.ConfigParser()
config.read("config.cfg")
DirBBDD = "integrity.db"


#Opciones disponibles de hash (por el momento)
opciones = {
    1 : 'md5',
    2 : 'sha1',
    3 : 'sha256'
}

#Metodo para comprobar que la BBDD no esta vacia
def compruebaBBDD(directorioBBDD):
    
    con = sqlite3.connect(directorioBBDD)
    cursor = con.cursor()
    
    BBDD = []
    cursor.execute('SELECT id, fileName, code from files')
    for i in cursor:
        BBDD += i;
    
    print(BBDD)
    

#Metodo para enviar email de notificacion
def enviarMail (mensaje):
    
    msg = MIMEText(mensaje)    
    
    MTo = config.get("SECTION2", "MailTo")
    MFrom = config.get("SECTION2", "MailFrom")
    password = config.get("SECTION2","PasswordFrom")
  
    msg['Subject'] = "Pérdida de integridad" 
    msg['From'] = MFrom
    msg['To'] = MTo 
    
    mailServer = SMTP('smtp.gmail.com',587)
    mailServer.ehlo() 
    mailServer.starttls() 
    mailServer.ehlo() 
    mailServer.login(MFrom,password)  

    mailServer.sendmail(MFrom, MTo, msg.as_string())

    mailServer.close()

#Metodo para cargar los datos de la BBDD a una lista
def cargaDatos(DirBBDD):
    
    con = sqlite3.connect(DirBBDD)
    cursor = con.cursor()
            
    BBDD = []
            
    cursor.execute('SELECT id, fileName, code from files')
    for i in cursor:
        BBDD += i;
    
    con.close()    
    return BBDD
    
    
#Metodo para comprobar la integridad de los archivos contenidos en un directorio,
#indicando el algoritmo a usar para hashear y el directorio de la BBDD
def compruebaIntegridad( dir , algoritmo ):
  
    con = sqlite3.connect(DirBBDD)
    cursor = con.cursor()
    noCumplen = []
    BBDD = cargaDatos(DirBBDD)
    
    if (len(dir) > 0):
            
        for directorios in dir :
        
            ficheros = os.walk(directorios)
            
            for (root, dirs, files) in ficheros: 
                for f in files:
                    
                    if (f.decode("utf-8") == "integrity.db"):
                        continue
                    if algoritmo == opciones.get(1): 
                        cod = hashlib.md5()
                    elif algoritmo == opciones.get(2):
                        cod = hashlib.sha1()
                    else:
                        cod = hashlib.sha256()
                    
                    h = open(os.path.join(root, f), "r", encoding = "ISO-8859-1")
                    contenido = h.read()
                    cod.update(contenido.encode("utf-8"))
                    digest = cod.hexdigest()
                    
                    if ( f in BBDD and digest in BBDD ): #Si no ha habido ninguna modificación se procede a comprobar el siguiente archivo
                        pass
                    
                    elif( f in BBDD and digest not in BBDD ): #Si el hash es modificado este notifica cual es el cambiado
                        noCumplen.append(f)  
                        print("El archivo " + f.decode("utf-8") + "ha sido modificado")
                        
                    elif ( f not in BBDD and digest not in BBDD ): #Si es un archivo nuevo lo introduce en la BBDD
                        params = (f, digest)
                        cursor.execute('INSERT INTO files (fileName, code) VALUES ( ?, ?)', params)
                        con.commit()
                        print("Se ha añadido un nuevo archivo con nombre : " + f.decode("utf-8") + "\n")
                        
                    del cod
                    h.close()
    else:
        print("Introduzca al menos un directorio")        
    
    numNoCumplen = len(noCumplen)
    
    if( numNoCumplen > 0 ):
        #Envio de email notificando que hay archivos modificados
        print("Hay " + str(numNoCumplen) + " archivos que han sido modificados." + "\n" + "\n")
        
        #Mensaje envidado por email
        mensaje = "Hola! \n \nEn la verificación de la integridad realizada: " + time.ctime() + "\n \nExisten " + str(numNoCumplen) + " archivos que han sido modificados." + "\n \n" + "Estos archivos son: " + str(noCumplen).decode("utf-8") + "\n \n" + "Este es un e-mail enviando desde Python" 
          
        enviarMail(mensaje);

        print("Email enviado correctamente \n")
       
    if(numNoCumplen == 0):
        return print("OK \n")
    con.close()   
    
    
#Metodo que ejecuta el verificador cada x minutos
def Timer(tiempo, directorio, algoritmo):
    minutos = tiempo
    sec = minutos * 60
    while True:
        compruebaIntegridad(directorio, algoritmo)
        time.sleep(sec)
        
        
        
        

if __name__ == '__main__':
   
    #Directorio a examinar
    directorio = []
    
    directorioConfig = config.items("PATHS")
    
    for key, path in directorioConfig:
        directorio.append(path.encode('utf_8'))
   
    #Tipo de algoritmo a usar
    algoritmo = config.get("SECTION1","Hash")
    
    #Tiempo de cada comprobacion
    tiempo = int(config.get("SECTION1","Time"))
    
    print('El resultado es:')
      
    #Metodo para temporizar la ejecucion
    Timer(tiempo, directorio, algoritmo)
    
    