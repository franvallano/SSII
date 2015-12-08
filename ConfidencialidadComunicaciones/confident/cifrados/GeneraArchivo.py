import os

def genera1Mb():
    
    f = open("1MB.txt", mode='w')
    
    while True:
        
        tam = os.path.getsize("1MB.txt")
        f.write("Prueba2-1MB-")
        
        if (tam == 1049984):
            break
        
    f.close()
    
def genera10Mb():
    
    f = open("10MB.txt", mode='w')
    
    while True:
        
        tam = os.path.getsize("10MB.txt")
        f.write("Prueba2-10MB-")
        
        if (tam == 10499840):
            break
        
    f.close()  

def genera20Mb():
    
    f = open("20MB.txt", mode='w')
    
    while True:
        
        tam = os.path.getsize("20MB.txt")
        f.write("Prueba2-20MB-")
        
        if (tam > 20999680):
            break
        print(tam)
        
    f.close() 

def genera10Kb():
    
    f = open("10KB.txt", mode='w')
    
    while True:
        
        tam = os.path.getsize("10KB.txt")
        f.write("Prueba2-10KB-")
        
        if (tam > 10240):
            break
        
    f.close() 
    
if __name__ == '__main__':
    
    genera1Mb()
    genera20Mb()