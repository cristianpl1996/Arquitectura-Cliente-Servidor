import zerorpc
import sys
import threading
import os
import eyed3
import json

myAddress = 'tcp://localhost:4243'
PLAYLIST = []

class NapsterClient(object):

	def __init__(self):
		self.uri = ''

	def getplaylist(self):
		self.dir = 'Lista1'
		for archivo in os.listdir(self.dir):
			audio = eyed3.load(os.path.join(self.dir,archivo))
			with open(os.path.join(self.dir,archivo), 'rb') as file:
				song = file.read()
			PLAYLIST.append({"Address": myAddress,"Titulo": audio.tag.title,
							 "Artista": audio.tag.artist, "Album": audio.tag.album, "Tamano": sys.getsizeof(song)})
			if os.path.isdir(os.path.join(self.dir,archivo)):
				__init__(os.path.join(self.dir,archivo))
	
	def importSong(self, uri):
		with open(uri, 'rb') as file:
			song = file.read()
		return song, sys.getsizeof(song)	

	def download(self, search, parts = 1, size = 0, sequential = 0):
		if (parts == 1):
			self.uri = 'Lista/' + search
			song, size = self.importSong(self.uri)
			return song
		else:
			self.uri = 'Lista/' + search
			song, size = self.importSong(self.uri)
			cuttingSize = size / parts
			rangeEnd = cuttingSize * sequential
			rangeStart = rangeEnd - cuttingSize
			x = 0
			with open('dir/temp', 'wb') as file:
				for data in song:
					if ((x >= rangeStart) and (x <= rangeEnd)):
						file.write(data)
					x += 1								
			songPart, size = self.importSong('dir/temp')
			return songPart

def main():
	while True:
		print ('Opciones: \n')
		print ('1. Descargar')
		print ('7. Salir \n')

		opcion = input('Digite Opcion: ')
		print('\n')

		if (int(opcion) == 7):
		    print('Bye')
		    break
		else:
			search = 'Fantasias.mp3'
			clientNapster = zerorpc.Client()
			clientNapster.connect('tcp://localhost:4242')
			size, address = clientNapster.search(search)
			clientNapster.importlistsong(PLAYLIST)
			for x in address:
				if (x == myAddress):
					address.remove(x)
			if (len(address) != 0):		
				if (len(address) == 1):
					client = zerorpc.Client()
					client.connect(address[0])
					song = client.download(search)
					with open('Lista1/Fantasias.mp3', 'wb') as file:
						for data in song:
							file.write(data)
						print('Descarga Terminada')
				else:
					parts = len(address)
					with open("Lista1/Fantasias.mp3", "wb") as file:
						for x in range(len(address)):
							sequential = x+1 
							client = zerorpc.Client()
							client.connect(address[x])
							songPart = client.download(search, parts, size, sequential)
							print (sys.getsizeof(songPart))
							for data in songPart:
								file.write(data)
							print( x+1, ' Parte Descargada')
			else:
				print ('No Hay Descarga')

def serverNapsterClient():
	serverClient = zerorpc.Server(NapsterClient())
	serverClient.getplaylist()
	serverClient.bind('tcp://0.0.0.0:4243')
	serverClient.run()
	
if __name__ == '__main__':
	execute = threading.Thread(target=main)
	execute.start()
	server = threading.Thread(target=serverNapsterClient)
	server.start()
	
	