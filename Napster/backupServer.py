import zerorpc
from pymongo import MongoClient 




class Napster(object):

	def __init__(self):
		self.uri = ''
		self.client = MongoClient('localhost',27017) 
		self.db = self.client.Napster
		self.collection = self.db.Songs
		self.collection.drop()
	
	def setPlayList(self, playList):
		L = []
	
		for i in playList:
			aux = []
			aux.append(i[0])
			L.append(dict([('puertos',aux),('titulo',i[1]),('artista',i[2]),('album',i[3]),('tamano',i[4])]))

		for i in L:
			lista = []
			puertos = []
			for k,v in i.iteritems():
				if k == 'puertos':
					for m in v:
						puertos.append(str(m))
				elif k == 'titulo':
					if self.collection.find_one({k:v}):
						item = self.collection.find_one({k:v})
						for j in item['puertos']:
							puertos.append(str(j))
						mj2 = list(set(puertos))
						aux = dict([('puertos',mj2),('titulo',str(item['titulo'])),('artista',str(item['artista'])),('album',str(item['album'])),('tamano',int(item['tamano']))])
						self.collection.remove({k:v})
						self.collection.insert(aux)	
					else:
						print 'guardado: ', self.collection.insert(i)
						break
				else:
					pass
	
	def search(self, filter, search):
		songs = []
		if (filter == 'Cancion'):
			for item in self.collection.find({'titulo':search}):
				song = []
				l=[]
				song.append(str(item['titulo'])+'.mp3')
				song.append(str(item['artista']))
				song.append(str(item['album']))
				song.append(item['tamano'])
				for i in item['puertos']:
					l.append(str(i))
				song.append(l)
				songs.append(song)		
		elif (filter == 'Artista'):
			for item in self.collection.find({'artista':search}):
				song = []
				l=[]
				song.append(str(item['titulo'])+'.mp3')
				song.append(str(item['artista']))
				song.append(str(item['album']))
				song.append(item['tamano'])
				for i in item['puertos']:
					l.append(str(i))
				song.append(l)
				songs.append(song)			
		elif (filter == 'Album'):
			for item in self.collection.find({'album':search}):
				song = []
				l=[]
				song.append(str(item['titulo'])+'.mp3')
				song.append(str(item['artista']))
				song.append(str(item['album']))
				song.append(item['tamano'])
				for i in item['puertos']:
					l.append(str(i))
				song.append(l)
				songs.append(song)			
		return songs	

server = zerorpc.Server(Napster())
server.bind('tcp://0.0.0.0:4242')
server.run()
