import zerorpc
import pymongo




class Napster(object):

	def __init__(self):
		self.uri = ''
		self.client = MongoClient('localhost',27017) 
		self.db = self.client.Napster()
		self.collection = db.Songs

	def setPlayList(self, playList):
		L = []
		for i in playList:
			L.append(dict([('titulo',i[0]),('autor',i[1]),('album',i[2]),('tamano',i[3]),('puertos',i[4])]))

		for i in L:
			for k,v in i.iteritems():
				if self.collection.find_one({k:v}):
					print 'Cancion encontrada'
				else:
					print 'Cancion no encontrada'
					
				
	def search(self, filter, search):
		songs = []
		for x in self.db:
			if (filter == 'Cancion'):
				if (x[0] == search):
					songs.append(x)	
			elif (filter == 'Artista'):
				if (x[1] == search):
					songs.append(x)
			elif (filter == 'Album'):
				if (x[2] == search):
					songs.append(x)	
		return songs	

server = zerorpc.Server(Napster())
server.bind('tcp://0.0.0.0:4241')
server.run()


"""
[['amiga.mp3','Miguel Bose', 'Linda', 6357801,['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']],
				   ['auto rojo.mp3', 'Vilma Palma E Vampiros', '3980', 7415986, ['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']],
                   ['mojada.mp3', 'Vilma Palma E Vampiros', '3980', 10907744, ['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']],
                   ['verano traidor.mp3', 'Vilma Palma E Vampiros', '3980', 10079291, ['tcp://localhost:4243', 'tcp://localhost:4244']],
				   ['billie jean.mp3', 'Michael Jackson', 'Thriller', 7077184, ['tcp://localhost:4243', 'tcp://localhost:4245']],
                   ['beat it.mp3', 'Michael Jackson', 'Thriller', 6221803, ['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']],
                   ['thriller.mp3', 'Michael Jackson', 'Thriller', 7077184, ['tcp://localhost:4243', 'tcp://localhost:4245']],
				   ['fantasias.mp3', 'Lenny Tabarez', '', 8600150, ['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']]]


				if k == 'titulo':
					if v == 'Titulo2':
						print 'se encontro'
				elif k == 'autor':
					if v == 'Autor2':
						print 'se encontro'
				elif k == 'autor':
					if v == 'Autor2':
						print 'se encontro'
				elif k == 'autor':
					if v == 'Autor2':
						print 'se encontro'
				elif k == 'autor':
					if v == 'Autor2':
						print 'se encontro'
"""