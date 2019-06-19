def comprueba_log_secure():
	#AQUI PRIMERO EXTRAEMOS TODAS LAS ENTRADAS CON CONTRASEÑA INCORRECTA
	ip_contador = []
	# Se extrae del archivo secure las entradas con failed password.
	# Las mismas corresponden a intentos de acceso fallidos por SSH.
	archivo = os.popen('cat /var/log/secure | grep "Failed password"').read() 
	archivo = archivo.split(os.linesep)										  
	for linea_log in archivo[:-1]:
		if 'for invalid user' in linea_log:
			ip_temp = linea_log.split(' ')[12]	# Se extrae la ip que no pudo acceder 
		else: 
			ip_temp = linea_log.split(' ')[10]	# Se extrae la ip que no pudo acceder

		fecha = linea_log.split(' ')[0] + linea_log.split(' ')[1]
		ip_contador.append((fecha,ip_temp))

	#Creamos una dupla (ip, cantidad de intentos de acceso)
	contador_log_ip = [[x,ip_contador.count(x)] for x in set(ip_contador)]   
	for temp in contador_log_ip:
		if temp[1] > N: 	# Si una ip supera N=3 intentos de acceso, se genera la alarma correspondiente 
			mensaje = 'IP bloqueada por superar el limite de intentos de acceso al sistema por SSH!'
			fecha = time.strftime("%d/%m/%Y")
			hora = time.strftime("%H:%M:%S")
			entrada_access_log_sis = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + temp[0][1]  
			archivo = open('/var/log/hids/prevencion_hids.log', 'r+')
			if not entrada_access_log_sis in archivo.read().split(os.linesep):
				archivo.write(entrada_access_log_sis+'\n')
				os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
				pass_file = open("pass_file.txt")
				input_pass_file = pass_file.read().replace('\n','')
				pass_file.close()
				os.system("rm -rf pass_file.txt")
				msg['Subject'] = "ALARMA EN HIDS!"
				msg.attach(MIMEText(entrada_access_log_sis, 'plain'))
				server = smtplib.SMTP('smtp.gmail.com: 587') 
				server.starttls()
				server.login(msg['From'], input_pass_file)
				server.sendmail(msg['From'], msg['To'], msg.as_string()) 
				server.quit()
				#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
				mensaje_login = 'echo "\nUna IP supero los intentos de acceso! Revisar correo para mas info.\n" '
				os.system(mensaje_login)
				ip_bloqueadas.append(temp[0][1])
			# Al banear una IP le bloqueamos el tráfico, en este caso trafico de entrada (de esa IP a la máquina).
			os.system('iptables -A INPUT -s ' + temp[0][1] + ' -j DROP')
			archivo.close()

	usuario_cont = []
	archivo_interno = os.popen('cat /var/log/secure | grep "FAILED LOGIN"').read()
	archivo_interno = archivo_interno.split(os.linesep)
	for linea_log in archivo_interno[:-1]:
		if not 'User not known to the underlying authentication module' in linea_log:
			usr_tmp = linea_log.split(' ')[11]		# Se identifica al USUARIO que no pudo acceder 
			fecha = linea_log.split(' ')[0] + linea_log.split(' ')[1]
			usuario_cont.append((fecha,usr_tmp))

	contador_log_usr = [[x,usuario_cont.count(x)] for x in set(usuario_cont)]
	for temp in contador_log_usr:
		if temp[1] > N:		# Si un usuario supera N=3 intentos de acceso, se genera la alarma correspondiente.
			# SI NO ES ROOT ENTONCES SE CAMBIA LA CONTRASEÑA!
			if not 'root' in temp[0][1][:-1]:					 
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				nuevo_passw = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
				# CONTROLAR LAS DOBLES COMILLAS EN LA SIGUIENTE LINEA
				os.system('echo "' + temp[0][1][:-1] +':'+ nuevo_passw + '" | chpasswd')
				mensaje = 'Cambio de contraseña de usuario por superar limite de intentos de acceso al sistema!'
				entrada_access_log = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + temp[0][1][:-1]
				archivo = open('/var/log/hids/prevencion_hids.log', 'r+')
				# PARA EVITAR REGISTROS REPETIDOS, PREGUNTAMOS ANTES SI YA EXISTE EN PREVENCION_LOG
				if not entrada_access_log in archivo.read().split(os.linesep):
					archivo.write(entrada_access_log+'\n')
					os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
					pass_file = open("pass_file.txt")
					input_pass_file = pass_file.read().replace('\n','')
					pass_file.close()
					os.system("rm -rf pass_file.txt")
					msg['Subject'] = "ALARMA EN HIDS!"
					msg.attach(MIMEText(entrada_access_log, 'plain'))
					server = smtplib.SMTP('smtp.gmail.com: 587') 
					server.starttls()
					server.login(msg['From'], input_pass_file)
					server.sendmail(msg['From'], msg['To'], msg.as_string()) 
					server.quit()
					#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
					mensaje_login = 'echo "\nUn usuario supero los intentos de acceso! Revisar correo para mas info.\n" '
					os.system(mensaje_login)

				archivo.close()
			else: 
				# SI ES ROOT ENTONCES NOTIFICAMOS AL CORREO DE QUE ALGUIEN (SEA O NO INTRUSO) SUPERO EL LIMITE
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				mensaje = 'Usuario root supera limite de intentos de acceso al sistema!'
				entrada_access_log = fecha + ' ---> ' + hora + '\n\n' + mensaje + '\n * ' + temp[0][1][:-1] 
				archivo = open('/var/log/hids/alarmas_hids.log', 'r+')
				if not entrada_access_log in archivo.read().split(os.linesep):
					archivo.write(entrada_access_log+'\n')
					os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
					pass_file = open("pass_file.txt")
					input_pass_file = pass_file.read().replace('\n','')
					pass_file.close()
					os.system("rm -rf pass_file.txt")
					msg['Subject'] = "ALARMA EN HIDS!"
					msg.attach(MIMEText(entrada_access_log, 'plain'))
					server = smtplib.SMTP('smtp.gmail.com: 587') 
					server.starttls()
					server.login(msg['From'], input_pass_file)
					server.sendmail(msg['From'], msg['To'], msg.as_string()) 
					server.quit()
					#AVISAMOS EN LA TERMINAL QUE SE HA ENCONTRADO ALGO SOSPECHOSO.
					mensaje_login = 'echo "\nUsuario ROOT supero los intentos de acceso! Revisar correo para mas info.\n" '
					os.system(mensaje_login)

				archivo.close()

# comprueba_log_secure ()