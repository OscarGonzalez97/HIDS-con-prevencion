import os

def cuarentena(archivo):
    #Quitamos todos los archivos y ponemos solo lectura para el duenho
    os.system("chmod 400 "+ archivo)
    #Ponemos el archivo en carpeta oculta de cuarentena
    os.system("mv " + archivo + " /home/.cuarentena")
    print("\nEl archivo "+archivo+" fue puesto en cuarentena. \n")
#cuarentena("archivocuarentena")
