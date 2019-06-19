#!/usr/bin/python
import md5
import getpass
import hashlib
import string 
import os
from os import listdir
import psycopg2 as pgDB

os.system("openssl enc -aes-256-cbc -d -in bd_password.txt.enc -out bd_password.txt -k PASS")
archivoPassword = open("bd_password.txt")
input_pass=archivoPassword.read().replace('\n','')
archivoPassword.close()
os.system("rm -rf bd_password.txt")

pgDB_conexion = pgDB.connect(user='root', password=input_pass, dbname='hids')
cursor = pgDB_conexion.cursor()
cursor.execute("DROP TABLE IF EXISTS archivos_md5")
cursor.execute("CREATE TABLE archivos_md5(id SERIAL, direccion_archivo  VARCHAR(100), md5sum VARCHAR(100) )") # direcciones de archivos a ser verificadas
lista_rutas = ['/etc/passwd','/etc/shadow','/bin','/usr/bin','/usr/sbin']

def carga_archivos (lista_rutas):
	lista_dir =[] # Lista que usaremos para extraer la firma MD5 de cada archivo
	for ruta in lista_rutas:					
		if os.path.isdir(ruta):   				    # Analizamos si la ruta es un archivo o una carpeta.
		   lista_dir_aux = os.listdir(ruta)		    # Si es una CARPETA, prepara un vector con la direccion del archivo que vamos a analizar
		   for elemento_lista in lista_dir_aux:
		   		lista_dir.append(ruta + '/' + elemento_lista )
		else:										# Si es un ARCHIVO.
		   lista_dir = [ruta]						# la lista de direcciones preparamos como un elemento y es la direccion completa del archivo

		for direccion in lista_dir:					# Recorremos el vector. 
			archivo_temp = hashlib.md5((open(direccion)).read())
 			sum_md5 = str(archivo_temp.hexdigest()) # Obtenemos la sum_md5 de cada archivo para luego cargar a la base de datos y cambiamos a formato str
			try :
				# INSERTAMOS LAS FIRMAS EN LA TABLA DE archivos_md5 PARA SU POSTERIOR USO
				cursor.execute("INSERT INTO archivos_md5 (direccion_archivo, md5sum) VALUES (%s,%s)",(direccion, sum_md5))
			except pgDB.Error as error:
				print("Error: {}".format(error))
			pgDB_conexion.commit()

carga_archivos (lista_rutas)


def carga_users():
	try:
		cursor = pgDB_conexion.cursor()   				   # conectamos a la base de datos
		cursor.execute("DROP TABLE IF EXISTS users") 	   # borramos tabla si existe
		# creamos la tabla users donde se guardamos usuarios, ips, email, pass 
		cursor.execute("CREATE TABLE users(id SERIAL, usr VARCHAR(30), addr VARCHAR(30), email VARCHAR(30), pass VARCHAR(30))") 
	except:
		print "No se pudo acceder a la base de datos"
		return

	os.system("openssl enc -aes-256-cbc -d -in lista_usuarios.txt.enc -out lista_usuarios.txt -k PASS")
	archivo=open('lista_usuarios.txt','r') #Abre el archivo que contiene la lista de usuarios permitidos	

	lineas = archivo.read().split(os.linesep)

	for aux in lineas[:-1]:
		if(aux != ''):
			vec = aux.split(' ') #Parseamos los datos en un vector de 4 campos los cuales identifican cada uno de los datos a ser insertado
			try:        #Insertamos los datos en la base de datos users
				cursor.execute("INSERT INTO users ( usr, addr, email, pass) VALUES (%s,%s,%s,%s)",(vec[0],vec[1],vec[2],vec[3][:len(vec[3])-1]) )
			except pgDB.Error as error:
				print("Error: {}".format(error))
			pgDB_conexion.commit()
	archivo.close()
	# Borramos el archivo txt despues de utilizarlo, SIEMPRE.
	os.system("rm -rf lista_usuarios.txt")

carga_users()

def carga_sniffers():
	try:
		cursor = pgDB_conexion.cursor()						# Conectamos a la base de datos
		cursor.execute("DROP TABLE IF EXISTS sniffers")     # Borramos la tabla si es que ya existe
		# Creamos una tabla sniffers donde se guardan nombres de sniffers que guardamos en un archivo txt. 
		cursor.execute("CREATE TABLE sniffers(id SERIAL, sniffer_name VARCHAR(32) )") 
	except:
		print "No se pudo acceder a la base de datos para cargar sniffers"
		return

	file = open('lista_sniffers.txt','r')	# abrimos el archivo que contiene los nombres de los sniffers


	for line in file:						# recorremos el archivo linea por linea
		tamanho=len(line)-2
		sniff=line[:tamanho]
		#Insertamos los datos en la base de datos sniffers, donde las columnas son id, sniffer_name
		try:
			cursor.execute("INSERT INTO sniffers ( sniffer_name) VALUES ( %s) " ,(sniff, ) )
		except pgDB.Error as error:
			print("Error: {}".format(error))
		pgDB_conexion.commit()

	file.close()

	pgDB_conexion.close()


carga_sniffers()

pgDB_conexion.close()
