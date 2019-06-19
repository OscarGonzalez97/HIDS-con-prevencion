def comprueba_archivos_tmp():
	for dirpath,_,filenames in os.walk('/tmp/'):
		for f in filenames:
			# AGREGAR CUARENTENA Y ELIMINAR AMENAZA
			# si se encuentra un archivo ejecutable se genera la alarma correspondiente
			if (('.py' in f ) or ('.sh' in f ) or ('.exe' in f) or  ('.deb' in f ) or ('.rpm' in f)):
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				mensaje = "Archivo ejecutable detectado!"
				entrada_ejecutable = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + f  
				archivo=open('/var/log/hids/alarmas_hids.log', 'r+')
				if not entrada_ejecutable in archivo.read().split(os.linesep):
				archivo.write(entrada_ejecutable+'\n')
				os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
				pass_file = open("pass_file.txt")
				input_pass_file = pass_file.read().replace('\n','')
				pass_file.close()
				os.system("rm -rf pass_file.txt")
				msg['Subject'] = "ALARMA EN HIDS!"
				msg.attach(MIMEText(entrada_ejecutable, 'plain'))
				server = smtplib.SMTP('smtp.gmail.com: 587') 
				server.starttls()
				server.login(msg['From'], input_pass_file)
				server.sendmail(msg['From'], msg['To'], msg.as_string()) 
				server.quit()
				#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
				mensaje_ejecutable = 'echo "\nEjecutable detectado! Revisar correo para mas info.\n" '
				os.system(mensaje_ejecutable)
				archivo.close()

			else:
				# AQUI ABRIMOS EL ARCHIVO Y BUSCAMOS AL COMIENZO DEL ARCHIVO LOS CARACTERES # y ! PARA
				# IDENTIFICAR SI ES UN SCRIPT O NO.
				with open(filenames, "r") as f:
					lines = f.readlines()
					cadena = lines[0]
					for i in range(len(cadena)):
						letra = cadena[i]
						if letra == '#' and cadena[i+1] == '!':
							cuarentena(filenames)
							fecha = time.strftime("%d/%m/%Y")
							hora = time.strftime("%H:%M:%S")
							mensaje = "Archivo ejecutable detectado, se ha enviado a cuarentena!"
							entrada_ejecutable = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + f  
							archivo=open('/var/log/hids/alarmas_hids.log', 'r+')
							if not entrada_ejecutable in archivo.read().split(os.linesep):
								archivo.write(entrada_ejecutable+'\n')
								os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
								pass_file = open("pass_file.txt")
								input_pass_file = pass_file.read().replace('\n','')
								pass_file.close()
								os.system("rm -rf pass_file.txt")
								msg['Subject'] = "ALARMA EN HIDS!"
								msg.attach(MIMEText(entrada_ejecutable, 'plain'))
								server = smtplib.SMTP('smtp.gmail.com: 587') 
								server.starttls()
								server.login(msg['From'], input_pass_file)
								server.sendmail(msg['From'], msg['To'], msg.as_string()) 
								server.quit()
								#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
								mensaje_ejecutable = 'echo "\nEjecutable detectado! Revisar correo para mas info.\n" '
								os.system(mensaje_ejecutable)

							archivo.close()								

	for dirpath,_,filenames in os.walk('/var/tmp/'):
		for f in filenames:
			if (('.py' in f ) or ('.sh' in f ) or ('.exe' in f) or  ('.deb' in f ) or ('.rpm' in f)): # si se encuentra un archivo ejecutable se genera la alarma correspondiente
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				mensaje = "Archivo ejecutable detectado!"
				entrada_ejecutable = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + f  
				archivo=open('/var/log/hids/alarmas_hids.log', 'r+')
				if not entrada_ejecutable in archivo.read().split(os.linesep):
					archivo.write(entrada_ejecutable+'\n')
					os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
					pass_file = open("pass_file.txt")
					input_pass_file = pass_file.read().replace('\n','')
					pass_file.close()
					os.system("rm -rf pass_file.txt")
					msg['Subject'] = "ALARMA EN HIDS!"
					msg.attach(MIMEText(entrada_ejecutable, 'plain'))
					server = smtplib.SMTP('smtp.gmail.com: 587') 
					server.starttls()
					server.login(msg['From'], input_pass_file)
					server.sendmail(msg['From'], msg['To'], msg.as_string()) 
					server.quit()
					#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
					mensaje_ejecutable = 'echo "\nEjecutable detectado! Revisar correo para mas info.\n" '
					os.system(mensaje_ejecutable)

				archivo.close()

			else:
				# AQUI ABRIMOS EL ARCHIVO Y BUSCAMOS AL COMIENZO DEL ARCHIVO LOS CARACTERES # y ! PARA
				# IDENTIFICAR SI ES UN SCRIPT O NO.
				with open(filenames, "r") as f:
					lines = f.readlines()
					cadena = lines[0]
					for i in range(len(cadena)):
						letra = cadena[i]
						if letra == '#' and cadena[i+1] == '!':
							cuarentena(filenames)
							fecha = time.strftime("%d/%m/%Y")
							hora = time.strftime("%H:%M:%S")
							mensaje = "Archivo ejecutable detectado, se ha enviado a cuarentena!"
							entrada_ejecutable = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + f  
							archivo=open('/var/log/hids/alarmas_hids.log', 'r+')
							if not entrada_ejecutable in archivo.read().split(os.linesep):
								archivo.write(entrada_ejecutable+'\n')
								os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
								pass_file = open("pass_file.txt")
								input_pass_file = pass_file.read().replace('\n','')
								pass_file.close()
								os.system("rm -rf pass_file.txt")
								msg['Subject'] = "ALARMA EN HIDS!"
								msg.attach(MIMEText(entrada_ejecutable, 'plain'))
								server = smtplib.SMTP('smtp.gmail.com: 587') 
								server.starttls()
								server.login(msg['From'], input_pass_file)
								server.sendmail(msg['From'], msg['To'], msg.as_string()) 
								server.quit()
								#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
								mensaje_ejecutable = 'echo "\nEjecutable detectado! Revisar correo para mas info.\n" '
								os.system(mensaje_ejecutable)

							archivo.close()	


# comprueba_archivos_tmp ()