import zerorpc
import sys

clientNapster = zerorpc.Client()
clientNapster.connect('tcp://localhost:4242')

class NapsterClient(object):

	def __init__(self):
		self.uri = ''

	def importSong(self, uri):
		with open(uri, 'rb') as file:
			song = file.read()
		return song, sys.getsizeof(song)	

	def download(self, search, parts = 1, size = 0, sequential = 0):
		if (parts == 1):
			self.uri = 'Lista2/' + search
			song, size = self.importSong(self.uri)
			return song
		else:
			self.uri = 'Lista2/' + search
			song, size = self.importSong(self.uri)
			cuttingSize = size / parts
			rangeEnd = cuttingSize * sequential
			rangeStart = rangeEnd - cuttingSize
			x = 0;
			with open('dir2/temp', 'wb') as file:
				for data in song:
					if ((x >= rangeStart) and (x <= rangeEnd)):
						file.write(data)
					x += 1								
			songPart, size = self.importSong('dir2/temp')
			return songPart

def main():
	while True:
		print 'Opciones: \n'
		print '1. Descargar'
		print '7. Salir \n'

		opcion = input('Digite Opcion: ')
		print('\n')

		if (int(opcion) == 7):
		    print('Bye')
		    break
		else:
			search = 'tosend.mp3'
			size, address = clientNapster.search(search)
			if (len(address) == 1):
				client = zerorpc.Client()
				client.connect(address[0])
				song = client.download(search)
				with open('Descargas/torecv.mp3', 'wb') as file:
					for data in song:
						file.write(data)
					print 'Descarga Terminada'
			else:
				parts = len(address)
				with open("Descargas/torecv.mp3", "wb") as file:
					for x in xrange(len(address)):
						sequential = x+1 
						client = zerorpc.Client()
						client.connect(address[x])
						songPart = client.download(search, parts, size, sequential)
						print sys.getsizeof(songPart)
						for data in songPart:
							file.write(data)
						print x+1, ' Parte Descargada'
			
if __name__ == '__main__':
	#main()
	serverClient = zerorpc.Server(NapsterClient())
	serverClient.bind("tcp://0.0.0.0:4244")
	serverClient.run()
	