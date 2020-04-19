import zerorpc

class Napster(object):

	def __init__(self):
		self.uri = ''
		self.db = [['amiga.mp3','Miguel Bose', 'Linda', 6357801,['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']],
				   ['auto rojo.mp3', 'Vilma Palma', '3980', 7415986, ['tcp://localhost:4243', 'tcp://localhost:4244']],
				   ['billie jean.mp3', 'Michael Jackson', 'Thriller', 7077184, ['tcp://localhost:4243', 'tcp://localhost:4245']],
				   ['fantasias.mp3', 'Lenny Tabarez', '', 6357801, ['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']]]

	def search(self, filter, search):
		for x in self.db:
			if (x[0] == search):
				name = x[0]
				artist = x[1]
				album = x[2]
				size = x[3]
				address = x[4]
				return name, artist, album, size, address	
		return 0, 0, 0, 0, 0
			
server = zerorpc.Server(Napster())
server.bind('tcp://0.0.0.0:4242')
server.run()
