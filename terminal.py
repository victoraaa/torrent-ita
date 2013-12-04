#coding: utf-8

import os

from client_download import download_file_view, list_files, register_as_owner

print "\n\n"
print "--- Torrent-ITA ---"
print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
print "\n\n"

# register_all_files_availables
for f in os.listdir('./files'):
	register_as_owner(f)

# Runs the command line forever
while True:
	#gets the user input
	command = raw_input()
	#the LIST_FILES command
	if command == "LIST_FILES":
		list_files()
	else:
		try:
			#the DOWNLOAD command
	 		if command.split(' ')[0] == "DOWNLOAD":
				download_file_view(command.split(' ')[1])
			else:
				#logs an error
				print ""
				print "Comando não aceito."
				print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
				print "\n\n"
		#logs an error
		except:
			print ""
			print "Comando não aceito."
			print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
			print "\n\n"
