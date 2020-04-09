import zerorpc

class Napster(object):

	def __init__(self):
		self.uri = ''
		self.db = [['Fantasias.mp3', 6357801, ['tcp://localhost:4243', 'tcp://localhost:4244', 'tcp://localhost:4245']]]

	def search(self, search):
		for x in self.db:
			if (x[0] == search):
				print("Se encontró\n")
				size = x[1]
				address = x[2]
			else: 
				size = 0
				address = " "
			return size, address
	
	def importlistsong(self, lista):
		print(lista)
			
server = zerorpc.Server(Napster())
server.bind('tcp://0.0.0.0:4242')
server.run()

#https://medium.com/@MicroPyramid/mongodb-crud-operations-with-python-pymongo-a26883af4d09