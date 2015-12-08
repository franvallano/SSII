import hmac
import itertools
import codecs
import time

mensaje = "CuentaOrigen_12345_a_CuentaDestino_67890_la_cantidad_de_3000_euros"

mac = "8b6a017282290f4ec9a26598bbdc93d2d09094f0"

def tipoHash(password):
    
    tam = len(password)
    
    if(tam == 32):
        hash = "md5"
    elif(tam == 40):
        hash = "sha1" 
    elif(tam == 56):
        hash = "sha224"
    elif(tam == 64):
        hash = "sha256"
    elif(tam == 96):
        hash = "sha384"
    else:
        hash = "sha512"
    
    return hash


def hack(code):
    
    inicio = time.time()
    
    h = tipoHash(code)
    
    msg = mensaje.encode('utf_8')
    
    l = "abcdef1234567890"
    
    #generar secuencia de 6 caracteres en hexadecimal
    for seq in itertools.product( l , repeat = 6):
        
        key = "".join(seq)
        
        #traducimos de hexadecimal a datos binarios
        p=codecs.decode(key ,"hex")
        
        digest_maker = hmac.new( p , msg , h).hexdigest()
    
        if (hmac.compare_digest(code,digest_maker)):
            
            print ("La contraseña es: " + key)
            break
        
        del digest_maker
        
    fin = time.time()    
    
    tiempo_total = fin - inicio
    
    print( "Tiempo de ejecucion : " + str(tiempo_total) ) 
    
    
if __name__ == '__main__':
    

    hack(mac)
    