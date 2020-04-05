import zerorpc

class Napster(object):

	def __init__(self):
		self.uri = ''
		self.db = [['tosend.mp3', 6357801, ['tcp://localhost:4245']]]

	def search(self, search):
		for x in self.db:
			if (x[0] == search):
				size = x[1]
				address = x[2]
			return size, address
			
server = zerorpc.Server(Napster())
server.bind('tcp://0.0.0.0:4242')
server.run()
