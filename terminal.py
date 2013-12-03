#coding: utf-8

from client_download import download_file_view, list_files

print "\n\n"
print "--- Torrent-ITA ---"
print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
print "\n\n"

while True:
	command = raw_input()
	if command == "LIST_FILES":
		list_files()
	else:
		try:
	 		if command.split(' ')[0] == "DOWNLOAD":
				download_file_view(command.split(' ')[1])
			else:
				print ""
				print "Comando não aceito."
				print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
				print "\n\n"
		except:
			print ""
			print "Comando não aceito."
			print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
			print "\n\n"