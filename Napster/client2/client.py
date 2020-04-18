#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
import tkMessageBox
import zerorpc
import sys
import threading
import pygame

inputDict = {}
addressServers = ['tcp://localhost:4241', 'tcp://localhost:4242']
global addressServer
addressServer = addressServers[0]
myAddress = 'tcp://localhost:4245'

class NapsterClient(object):

	def __init__(self):
		self.uri = ''

	def importSong(self, uri):
		with open(uri, 'rb') as file:
			song = file.read()
			file.close()
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
			x = 0;
			with open('dir/temp', 'wb') as file:
				for data in song:
					if ((x >= rangeStart) and (x <= rangeEnd)):
						file.write(data)
					x += 1
				file.close()								
			songPart, size = self.importSong('dir/temp')
			return songPart

def serverNapsterClient():
	serverClient = zerorpc.Server(NapsterClient())
	serverClient.bind('tcp://0.0.0.0:4245')
	serverClient.run()

def main():
	root = Tk()
	root.geometry('700x450')
	root.title('Napster  ©')
	root.resizable(0,0)
	icon = root.iconbitmap('images/icon.ico')      
	background = PhotoImage(file = 'images/napster.gif')
	background1 = PhotoImage(file = 'images/napsterd.gif')
	Background = Label(root, image = background)
	Background.place(x = -2, y = -2)
	txt = Entry(root, width = 40)
	txt.place(x = 230, y = 210)
	combo = Combobox(root, width = 15)
	combo['values'] = ('Cancion', 'Artista', 'Album')
	combo.place(x = 105, y = 210)
	combo.current(0)
	frame = Frame(root, width = 601, height = 150)
	frame.place(x = 40, y = 275)
	canvas = Canvas(frame, bg = 'white', width = 603, height = 150)
	canvas.pack(side = 'left', fill = 'both')
	scrollbar = Scrollbar(frame, orient = 'vertical', command = canvas.yview)
	scrollbar.pack(side = 'right', fill = 'y')
	scrollable_frame = Frame(canvas, width = 601, height = 150)
	scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
	canvas.create_window((0, 0), window = scrollable_frame, anchor = "nw")
	canvas.configure(yscrollcommand = scrollbar.set)
	col = Button(root, width = 15, text = 'Canción', state = 'disable')
	col.place(x = 40, y = 250)
	col1 = Button(root, width = 15, text = 'Artista', state = 'disable')
	col1.place(x = 140, y = 250)
	col2 = Button(root, width = 15, text = 'Album', state = 'disable')
	col2.place(x = 240, y = 250)
	col3 = Button(root, width = 15, text = 'Tamaño', state = 'disable')
	col3.place(x = 340, y = 250)
	col4 = Button(root, width = 15, text = 'Host', state = 'disable')
	col4.place(x = 440, y = 250)
	col5 = Button(root, width = 19, text = 'Acción', state = 'disable')
	col5.place(x = 540, y = 250)
	canvasBox = Canvas(scrollable_frame, bg = 'white', width = 1000, height = 2000)
	canvasBox.pack()

	def playMusic(uri, btn, btn1):
		btn.configure(state = 'disabled')
		btn1.configure(state = 'enabled')
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.music.load(uri)
		pygame.mixer.music.play()

	def stopMusic(btn, btn1):
	    pygame.mixer.music.stop()
	    pygame.mixer.quit()
	    pygame.quit()
	    btn.configure(state = 'enabled')
	    btn1.configure(state = 'disabled')

	def createChildRoot(search, uri):
   		childRoot = Toplevel(root)
   		childRoot.geometry('300x165')
		childRoot.title('Reproductor ©')
		childRoot.resizable(0,0)
		icon = childRoot.iconbitmap('images/icon.ico')
		Background = Label(childRoot, image = background1)
		Background.place(x = -2, y = -2)
		txt = Label(childRoot, text = search)
		txt.place(x = 110, y = 100)
		btn = Button(childRoot, width = 15, text = 'Play')
		btn.place(x = 50, y = 130)
		btn1 = Button(childRoot, width = 15, text = 'Stop', )
		btn1.place(x = 150, y = 130)
		btn.configure(command = lambda uri =  uri, btn =  btn, btn1 =  btn1 : playMusic(uri, btn, btn1))
		btn1.configure(command = lambda btn =  btn, btn1 =  btn1  : stopMusic(btn, btn1))
		playMusic(uri, btn, btn1)
			
	def deleteDict():
		inputDict = {}
		
	def download(search, size, address):
		pygame.mixer.quit()
		pygame.quit()
		if (len(address) == 1):
			client = zerorpc.Client()
			client.connect(address[0])
			song = client.download(search)
			with open('Descargas/' + search, 'wb') as file:
				for data in song:
					file.write(data)
				print 'Descarga Terminada'
				file.close()
		else:
			parts = len(address)
			with open('Descargas/' + search, 'wb') as file:
				for x in xrange(len(address)):
					sequential = x + 1 
					client = zerorpc.Client()
					client.connect(address[x])
					songPart = client.download(search, parts, size, sequential)
					print sys.getsizeof(songPart)
					for data in songPart:
						file.write(data)
					print x+1, ' Parte Descargada'
				print 'Descarga Terminada'
				file.close()
		createChildRoot(search, 'Descargas/' + search)

	def downloadAlbum(songs):
		pygame.mixer.quit()
		pygame.quit()
		for x in songs:
			search = x[0],
			size = x[3], 
			address = x[4]
			download(search[0], size[0], address)

	def search():
		global addressServer
		deleteDict()
		search = txt.get()
		if len(search) == 0:
			tkMessageBox.showerror('Información ©', 'Digite busqueda a realizar.')
		else:
			try:
				filter = combo.get()
				if (filter == 'Cancion'):
					search = search + '.mp3'
				clientNapster = zerorpc.Client()
				clientNapster.connect(addressServer)
				songs = clientNapster.search(filter, search)
				if (len(songs) > 0):
					for x in songs:
						for y in x[4]:
							if (y == myAddress):
								x[4].remove(y)
					
					canvasBoxChild = Canvas(canvasBox, bg = 'white', width = 1000, height = 2000)
					canvasBoxChild.place(x=0, y=0)
					i, y = 1, 2
					for x in songs:
						if (len(x[4]) != 0):
							inputDict[i] = Entry(canvasBoxChild, width = 15)
							inputDict[i].place(x = 2, y = y)
							inputDict[i].insert(0, x[0])
							inputDict[i].config(state="readonly")
							inputDict[i+1] = Entry(canvasBoxChild, width = 15)
							inputDict[i+1].place(x = 102, y = y)
							inputDict[i+1].insert(0, x[1])
							inputDict[i+1].config(state="readonly")
							inputDict[i+2] = Entry(canvasBoxChild, width = 15)
							inputDict[i+2].place(x = 202, y = y)
							inputDict[i+2].insert(0, x[2])
							inputDict[i+2].config(state="readonly")
							inputDict[i+3] = Entry(canvasBoxChild, width = 15)
							inputDict[i+3].place(x = 302, y = y)
							inputDict[i+3].insert(0, x[3])
							inputDict[i+3].config(state="readonly")
							inputDict[i+4] = Entry(canvasBoxChild, width = 15)
							inputDict[i+4].place(x = 402, y = y)
							inputDict[i+4].insert(0, 'Clientes: ' + str(len(x[4])))
							inputDict[i+4].config(state="readonly")
							inputDict[i+5] = Button(canvasBoxChild, width = 15, text = 'Descargar', command = lambda search = x[0], size =  x[3], address =  x[4] : download(search, size, address))
							inputDict[i+5].place(x = 502, y = y-2)
							i+=6
							y+=25
					if (filter == 'Album'):
						albumDownload = Button(canvasBoxChild, width = 98, text = 'Descargar Album', command = lambda songs = songs: downloadAlbum(songs))
						albumDownload.place(x = 3, y = y-2)
				else:
					tkMessageBox.showerror('Información ©', 'No se han encontrado resultados para tu búsqueda(' + search + ').')		
				txt.delete(0, END)
			except zerorpc.exceptions.LostRemote as e:
				addressServer = addressServers[1]
				tkMessageBox.showerror('Información ©', 'Tuvimos un error intentalo de nuevo.')
		
	btn = Button(root, width = 15, text = 'Buscar', command = search)
	btn.place(x = 490, y = 208)
	root.mainloop()

if __name__ == '__main__':
	execute = threading.Thread(target = main)
	execute.start()
	server = threading.Thread(target = serverNapsterClient)
	server.start()
