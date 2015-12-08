__author__ = "Fco. Javier Delgado Vallano"
__copyright__ = "Copyright (C) 2005 Fco. Javier Delgado Vallano"

# -*- coding: utf-8 -*-
import hashlib
import sqlite3 
import os
import configparser

config = configparser.ConfigParser()
config.read("config.cfg")
DirBBDD = "integrity.db"

con = sqlite3.connect( DirBBDD )
cursor = con.cursor()

cursor.execute('DROP TABLE IF EXISTS files')
cursor.execute('CREATE TABLE files (id integer primary key, fileName text, code text)')

con.close()


#Opciones disponibles de hash (por el momento)
opciones = {
    1 : 'md5',
    2 : 'sha1',
    3 : 'sha256'
}


def archivosEnDirectorio(dir,algoritmo):
    

    con = sqlite3.connect(DirBBDD)
    cursor = con.cursor()
    msgFinal = 'BBDD creada correctamente'
    
    if (len(dir) > 0):
        
        for directorios in dir :
            
            ficheros = os.walk(directorios)
            
            for (root, dirs, files) in ficheros: 
                for f in files:   
                    
                    if (f.decode("ISO-8859-1") == "integrity.db"):
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
                    
                    #Insertar en la BBD
                    params = (f, digest)
                    cursor.execute('INSERT INTO files (fileName, code) VALUES ( ?, ?)', params)
                    con.commit()
                    
                    del cod
                    h.close()
            
    else:
        
        msgFinal = "Introduzca al menos un directorio!!"
        
        
    print(msgFinal)
            
    con.close()
    

if __name__ == '__main__':

    #Directorio a examinar
    directorio = []
    
    directorioConfig = config.items("PATHS")
    
    for key, path in directorioConfig:
        directorio.append(path.encode('utf_8'))
    
    
    #Tipo de algoritmo a usar
    algoritmo = config.get("SECTION1", "Hash")
   
    
    #Llamada al método que para cargar la cara inicial
    archivosEnDirectorio(directorio, algoritmo)    
   
