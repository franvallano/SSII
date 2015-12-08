# -*- coding: utf-8 -*-
import hashlib

contra = "fdfba0e18f6c257f9c2e48575ed84b7568b3fceb680ece9620524df1d14603f2a6cd8130dd7a8c13da5314c68cc5655a"

#Metodo para identificar el metodo hashing utilizado
def tipoHash(password):
    tam = len(password)
    if(tam == 32):
        hash = hashlib.md5();
    elif(tam == 40):
        hash = hashlib.sha1() 
    elif(tam == 56):
        hash = hashlib.sha224()
    elif(tam == 64):
        hash = hashlib.sha256()
    elif(tam == 96):
        hash = hashlib.sha384()
    else:
        hash = hashlib.sha512()
    
    return hash


#Metodo utilizado para leer archivo qu contiene las palabras del diccionario
def leerDesdeArchivo(archivo):
    dic = []
    f = open(archivo, "r" , encoding="utf8")
    for line in f.readlines():
        line = line.replace("\n","")
        dic.append(line)
    f.close()
    return dic
    
 
#Metodo que comprueba la contraseña utilizada
def hack(passw):
    
    dic = leerDesdeArchivo("words.txt")
    hash = tipoHash(passw)
    
    
    for contenido in dic:
        hash = tipoHash(passw)
        
        hash.update(contenido.encode("utf-8"))            
        
        digest = hash.hexdigest()
        
        if (passw == digest):
            print(contenido)
            break
        
        del hash
    



if __name__ == '__main__':
    
    #Metodo para sacar contraseña
    print("La contraseña es: " + hack(contra))
    
   
    
    
   