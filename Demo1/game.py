import socket
import logging
import time
import pickle
import threading

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

class Msg:
	ip = ''
	port = 0
	name = ''
	status = ''
	x = 0;
	y = 0;
	def __init__(self, ip, port, name, status, x, y):
		self.ip = ip
		self.port = port
		self.name = name
		self.status = status
		self.x = x
		self.y = y

class Handler ( threading.Thread ):
	def __init__ (self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
	
	def run (self ):
		while True :
			client_msg = self.conn.recv(1024)
			message = client_msg
			if message != '':
				print 'Received data  :', message


class Player:
	logger = logging.getLogger('Player')
	name = ''
	ip = ''
	status = ''
	startX = 0
	startY = 0
	
	peerlist = []
	BC_PORT = 12345
	myport = 1234
#	global ip
	ip = socket.gethostbyname(socket.gethostname())
	
	def __init__(self,name = ''):
		self.name = name
		self.status = 'waiting'
		self.logger = logging.getLogger('Player')
		self.logger.debug('__init__')

	def getName(self):
		return self.name

	def getIp(self):
		return self.ip

	def setName(self, name):
		self.name = name

	def setIp(self, ip):
		self.ip = ip

	def setStatus(self):
		if self.status == 'waiting':
			self.status = 'ready'
		elif self.status == 'ready':
			self.status = 'waiting'

	def getStatus(self):
		return self.status

	def equals(self, rhs):
		if self.name == rhs.name and self.ip == rhs.ip:
			return True
		else:
			return False

	def initSnake(self, x, y):
		startX = x;
		startY = y;

	def main_func(self, choice):
		self.logger = logging.getLogger('Player')
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		address = (self.ip, self.myport)
		print address
		server_socket.bind(address)
		server_socket.setblocking(False)

		data = Msg(self.ip, self.myport, self.name, self.status, self.startX, self.startY)
		broadcastdata  = pickle.dumps(data)

		flag = True
		while flag:
			self.logger.debug('Choice1: "%s"', choice)
			if (choice == "1"):
				flag = False
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.bind(('', 0))
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				myaddr = (self.ip,self.myport)
				while (len(self.peerlist) < 1):
					begin = time.time()
					while ((time.time() - begin) < 10) :
						sock.sendto(broadcastdata, ('<broadcast>', self.BC_PORT))
						#print "Broadcast message sent"
						try :
							recv_data, addr = server_socket.recvfrom(2048)
							r_Msg = pickle.loads(recv_data)
							self.peerlist.append(r_Msg)
							print 'List:'
							for message in self.peerlist:
								print message.name
						except:
							pass
				sock.close()
			if (choice == "2"):
				# Receive a response
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				sock.bind(('', self.BC_PORT))
				sock.setblocking(False)
				begin = time.time()
				while ((time.time() - begin) < 10) :
					try :
						message, addr = sock.recvfrom(8192)
						flag = False
						break
					except:
						pass
				s_Msg = pickle.loads(message)
				print 'Sender Port '
				print s_Msg.port
				print 'Sender IP '
				print s_Msg.ip
				sender_address = (s_Msg.ip, int(s_Msg.port))
				print sender_address
				server_socket.sendto(broadcastdata, sender_address)
				print "Sent join"
				sock.close()
				
		server_socket.close()
		#start the server thread  
		server_thread =  Server(self.myport, int(choice))
		server_thread.start()

		#start client threads for all the players who responded

		print 'choice:', choice

		if (choice == "1"):
			num_other_players = len(self.peerlist)
			send_list = self.peerlist
			send_list.append(data)
			print self.peerlist
			for i in range(0,num_other_players) :
				peer_Msg = self.peerlist[i]
				client_thread = client(peer_Msg.ip, peer_Msg.port, send_list)
				client_thread.start()
        elif (choice == '2'):
            while (len(server_thread.getList()) == 0):
                pass
            self.peerlist = server_thread.getList()

class Table:
	horizonSize = 500
	verticalSize = 500

	name = ''
	players = {}

	def __init__(self, name = '', player = None):
		self.name = name
		self.players[self.getName()] = player

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def addPlayer(self, player):
		if player in self.players:
			return False
		else:
			self.players[player.getName()] = player
			return True

	def removePlayer(self, name):
		del self.players[name]

	def getPlayer(self, name):
		return self.players[name]

	def initSnake(self):
		x = len(self.players.keys())
		y = x // (x ** .5)
		x = (x + y - 1) // y
		i = -1;
		j = 0;
		for player in self.players.keys():
			i = i + 1
			if i == x:
				j = j + 1
				i = 0;
			self.players[player].initSnake(self.horizonSize * i / x + self.horizonSize / x / 2, 
				                           self.verticalSize * j / y + self.verticalSize / y / 2)

		for destPlayer in self.players.keys():
			destIp = self.players[destPlayer].getIp()
			for messagePlayer in self.players.keys():
				message = self.players[messagePlayer].getIp()
				#send(destIp, msg)
			#send(destIp, destPlayer)

	def setPlayerStatus(self, name):
		self.players[name].setStatus()
		flag = True
		for player in self.players.keys():
			if self.players[player].getStatus() != 'ready':
				flag = False
				break
		if flag:
			self.initSnake()

	def getPlayerNames(self):
		return self.players.keys()

	def printPlayer(self):
		for player in self.players.keys():
			print 'name %s : ip %s' % (self.players[player].getName(), self.players[player].getIp())

class Server(threading.Thread):
	tables = {}
    
    storage = []
    
    def getList(self):
        return self.storage
	
	def __init__(self, port, choice):
		threading.Thread.__init__(self)
		self.port = port
		self.creator = choice

	def run ( self ):
		print 'server run:'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', self.port))
		s.listen(5)
		if (self.creator == 1):
			while True :
				conn, addr = s.accept()
				print 'Accepted connection from '
				print addr
				handler = Handler(conn,addr)
				handler.start()
		else:
			conn, addr = s.accept()
			print 'Accepted connection from '
			print addr
			client_resp = conn.recv(1024)
			list_of_players = pickle.loads(client_resp)
			peerlist = list_of_players
			print 'List : '
            self.storage = peerlist
			for msg in peerlist:
				print msg.name
			for j in range(0,len(peerlist)):
				peer_Msg = peerlist[j]
				if (peer_Msg.port != self.port):
					client_thread = client(peer_Msg.ip, peer_Msg.port, "hi") 
					client_thread.start()
			while True:
				conn, addr = s.accept()
				print 'Accepted connection from '
				print addr
				handler = Handler(conn,addr)
				handler.start()

	def addTable(self, table):
		if table.getName() in self.tables:
			return False
		else:
			self.tables[table.getName()] = table
			return True

	def removeTable(self, tableName):
		del self.tables[tableName]

	def getTableNames(self):
		return self.tables.keys()

	def getTable(self, name):
		return self.tables[name]
	
class client(threading.Thread):
    def __init__(self, ip, port, data):
        threading.Thread.__init__(self)
        self.port = port
        self.host = ip # Get local machine name
        self.data = data
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
    def run(self):
        print 'Connecting to ', self.host, self.port
        self.clientSock.connect((self.host, self.port))      
        send_data  = pickle.dumps(self.data)
        self.clientSock.send(send_data)

