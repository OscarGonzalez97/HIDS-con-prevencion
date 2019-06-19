def comprueba_archivos (lista_rutas):
	lista_dir =[]  # LISTA DONDE ALMACENAREMOS LAS RUTAS ABSOLUTAS DE LOS ARCHIVOS A ANALIZAR CON FIRMA MD5			
	for ruta in lista_rutas:					
		if os.path.isdir(ruta):  #se analiza si la ruta es un archivo o una carpeta, si es una carpeta, se prepara el vector con la direccion absoluta de los archivos a analizar
			lista_dir_temp = os.listdir(ruta)
			for elemento_lista in lista_dir_temp:
				lista_dir.append(ruta + '/' + elemento_lista )
		else:	#si no, simplemente se prepara la lista como una de un elemento, la direccion abusoluta del unico archivo
			lista_dir = [ruta]

		for direccion in lista_dir:	 #se recorre el vector, se obtiene la suma md5 correspondiente a cada archivo, y se carga en la bd
			archivo_temp = hashlib.md5((open(direccion)).read())
			sumamd5 = str(archivo_temp.hexdigest())   
			try :
				cursor.execute("SELECT direccion_archivo FROM archivos_md5 WHERE direccion_archivo=%s", (direccion,))
				check_existe = cursor.fetchone()
				if isinstance(check_existe, tuple):   #Si existe el archivo buscado en la base de datos.
					cursor.execute("SELECT md5sum FROM archivos_md5 WHERE direccion_archivo=%s",(direccion,))
					check_md5= cursor.fetchone()[0]
					if check_md5 != sumamd5:		       #Se verifica que el archivo consultado y el archivo de la base de datos tengan la misma
						fecha = time.strftime("%d/%m/%Y")  #firma md5, si no tienen la misma firma se genera la alarma correspondiente.
						hora = time.strftime("%H:%M:%S")      
						mensaje = 'Archivo modificado: '	 
						entrada_archivos = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + direccion  
						archivo=open('/var/log/hids/alarmas_hids.log', 'r+')
						if not entrada_archivos in archivo.read().split(os.linesep):
							archivo.write(entrada_archivos+'\n')

							#MANDAMOS CORREO AL ADMIN PARA ALERTAR DE POSIBLE AMENAZA CON EL USO DE SMTP
							#ESTE CODIGO SE REPETIRA EN VARIOS MODULOS, SOLO AQUI SE EXPLICA.
							os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
							pass_file = open("pass_file.txt")
							input_pass_file = pass_file.read().replace('\n','')
							pass_file.close()
							os.system("rm -rf pass_file.txt")
							msg['Subject'] = "ALARMA EN HIDS!"
							msg.attach(MIMEText(entrada_archivos, 'plain'))
							server = smtplib.SMTP('smtp.gmail.com: 587') 
							server.starttls()
							server.login(msg['From'], input_pass_file)
							server.sendmail(msg['From'], msg['To'], msg.as_string()) 
							server.quit()
							#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
							mensaje_md5 = 'echo "\nFirma MD5 distinta! Revisar correo para mas info.\n" '
							os.system(mensaje_md5)

						archivo.close()
				else:			#Si no existe el archivo buscado en la base de datos, se genera la alarma correspondiente
						mensaje = 'El archivo no esta cargado en la base de datos!'
						entrada_archivos = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + direccion 
						archivo=open('/var/log/hids/alarmas_hids.log', 'r+')
						if not entrada_archivos in archivo.read().split(os.linesep):
							archivo.write(entrada_archivos+'\n')

							os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
							pass_file = open("pass_file.txt")
							input_pass_file = pass_file.read().replace('\n','')
							pass_file.close()
							os.system("rm -rf pass_file.txt")
							msg['Subject'] = "ALARMA EN HIDS!"
							msg.attach(MIMEText(entrada_archivos, 'plain'))
							server = smtplib.SMTP('smtp.gmail.com: 587') 
							server.starttls()
							server.login(msg['From'], input_pass_file)
							server.sendmail(msg['From'], msg['To'], msg.as_string()) 
							server.quit()
							mensaje_md5 = 'echo "\nUn archivo no existe en la Base de Datos! Revisar correo para mas info.\n" '
							os.system(mensaje_md5)						

						archivo.close()

			except :
				print("Error")