#coding: utf-8

from client_download import download_file_view, list_files_view

print "\n\n"
print "--- Torrent-ITA ---"
print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
print "\n\n"

while True:
	command = raw_input()
	if command == "LIST_FILES":
		pass
	elif command.split(' ')[0] == "DOWNLOAD":
		pass
	else:
		print ""
		print "Comando não aceito."
		print "Comandos disponíveis: LIST_FILES e DOWNLOAD <FILENAME>"
		print "\n\n"
