import socket
import logging
import time
import pickle
import threading
from node import *
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

class Msg:
	ip = ''
	port = 0
	name = ''
	node = None
	data = ''
	msg_type = ''
	peerlist = []

	def __init__(self, ip, port, name = '', data = '', msg_type = '', node = None, peerlist = None):
		self.ip = ip
		self.port = port
		self.name = name
		self.data = data
		self.msg_type = msg_type
		self.node = node
		self.peerlist = peerlist

class Handler ( threading.Thread ):
    def __init__ (self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run (self ):
        while True :
            client_msg = self.conn.recv(5000)
            '''
            TODO: Receive the message object
             message = pickle.loads(client_msg)
             message.data == "Restart"
             update score 
             if any persons score is MAX SCORE
                 display score and go to main screen
             else
                 wait for 3 seconds
             start round
            ''' 
            message = pickle.loads(client_msg)
            if message.data != '':
                print 'Received data  :', message.data  

class Player:
	name = ''
	ip = socket.gethostbyname(socket.gethostname())
	myport = 1238
	BC_PORT = 12345
	peerlist = []
	client_obj_list = []
	
	node = None
	direction = 0
	color = 0
	
	def __init__(self, name = ''):
		self.name = name

	def getName(self):
		return self.name

	def getIp(self):
		return self.ip

	def setName(self, name):
		self.name = name

	def setIp(self, ip):
		self.ip = ip

	def get_client_thr_obj(self, ip, port):
		for k in range(0, len(self.client_obj_list)):
			if ((ip == self.client_obj_list[k].ip) and (port == self.client_obj_list[k].port)):
				return self.client_obj_list[k]

	def send_msg_to_list(self, lst):
		for msg in lst:
			client_obj = self.get_client_thr_obj(msg.ip, msg.port)
			client_obj.send(msg)

	def equals(self, rhs):
		if self.name == rhs.name and self.ip == rhs.ip and self.myport == rhs.myport:
			return True
		else:
			return False

	def main_func(self, choice):
		self.logger = logging.getLogger('Player')
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		address = (self.ip, self.myport)
		print address
		server_socket.bind(address)
		server_socket.setblocking(False)

		mydata = Msg(self.ip, self.myport, self.name, 'b_data', 'broadcast')
		broadcastdata  = pickle.dumps(mydata)

		flag = True
		while flag:
			self.logger.debug('Choice: "%s"', choice)
			# Player has chosen to send broadcast (start the game)
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
						'''
						Broadcast message sent
						Wait for 10 seconds, minimum, or wait until atleast 1
						person joins the game.
						'''
						try :
							recv_data, addr = server_socket.recvfrom(2048)
							r_Msg = pickle.loads(recv_data)
							''' 
							peerlist contains the list of all peers who responded to the
							BC_message. 
							'''
							self.peerlist.append(r_Msg)
							print 'List:'
							for message in self.peerlist:
								print message.name
						except:
							pass
					sock.close()
                
			# Player has chosen to receive broadcast (join the game)
			if (choice == "2"):
				# Receive a response
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				sock.bind(('', self.BC_PORT))
				sock.setblocking(False)
				begin = time.time()
				'''
				If the player has not received a broadcast (able to join a game)
				within 10 seconds
				'''
				while ((time.time() - begin) < 10) :
					try :
						message, addr = sock.recvfrom(8192)
						flag = False
						break
					except:
						pass

				if message != '':
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
		server_thread =  Server(self.ip, self.myport, int(choice))
		server_thread.start()

		'''
		If the player has chosen to start the game, start client threads for all 
		the players who responded.

		'''        
		if (choice == "1"):
			num_other_players = len(self.peerlist)
			send_list = self.peerlist
			send_list.append(mydata)
			print self.peerlist

			#send the list            
			for i in range(0,num_other_players) :
				peer_Msg = self.peerlist[i]
				client_thread = client(peer_Msg.ip, peer_Msg.port)
				self.client_obj_list.append(client_thread)
				client_thread.start()
                
			time.sleep(1);

            #send the list of all players (including self) to all the clients in my client list

			table = Table()
			for msg in self.peerlist:
				newPlayer = Player(msg.name)
				newPlayer.ip = msg.ip
				newPlayer.myport = msg.port
				table.addPlayer(newPlayer)

			table.initSnake()

			self.node = table.getPlayer(self.name).node

			for j in range(0, len(self.peerlist)):
				peer_Msg = self.peerlist[j]
				if ((peer_Msg.ip == self.ip) and (peer_Msg.port == self.myport)):
					continue
				else:
					client_obj = self.get_client_thr_obj(peer_Msg.ip, peer_Msg.port)
					msg = Msg(None, None, None, 'player_list', 'unicast', table.getPlayer(peer_Msg.name).node, send_list)
					client_obj.send(msg)
		else:
			# Wait until you get the list of players from the starter
			while server_thread.getMsg() == None:
				time.sleep(0.01)

			msg = server_thread.getMsg()
			self.node = msg.node
			self.peerlist = msg.peerlist
			'''
			TODO: Once you have the list of players, wait for 5 seconds and start the game
			'''

		print 'WTF!!!!!!!!'
		print self.node.name
		print self.node.head.x
		print self.node.head.y
		print self.node.direction

		#time.sleep(5);          

		#keep playing as long as you dont win or lose
#		iWon = 0
#		while True:
#			if server_thread.getMsg() != None:
#				msg = server_thread.getMsg()
#				print 'msg', msg.data
#				if msg.data == 'update':
#					self.node.receive(msg.node)
#					server_thread.popMsg()
#
#			print 'start update'
#			self.node.show()
#			#iWon = self.node.update(self.direction, self.color)
#
#			lst = []
#			for nId in self.node.neighbors.keys():
#				n = self.node.neighbors[nId]
#				msg = Msg(n.ip, n.port, None, 'update', 'multicast', self.node, None)
#				lst.append(msg)
#
#			print 'send to list'
#			self.send_msg_to_list(lst)
#
#			if (iWon != 0):
#				break 
#			time.sleep(0.05)

		# You won. So calculate the score for every1 and multicast a restart message
		#if (iWon == 1):
			#calculate_score(mynode)  

class Table:
	height = 500
	width = 500

	players = {}

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
		print 'initSnake'
		x = len(self.players.keys())
		y = x // (x ** .5)
		x = (x + y - 1) // y
		i = -1;
		j = 0;
		counter = -1
		nmap = []
		for player in self.players.keys():
			counter = counter + 1
			i = i + 1
			if i == x:
				j = j + 1
				i = 0;
			head = Point(self.height * i / x + self.height / x / 2, self.width * j / y + self.width / y / 2)
			r = Rectangle()
			r.tl = Point(self.height * i / x, self.width * j / y)
			r.br = Point(self.height * i / x + self.height / x, self.width * j / y + self.width / y)
			rs = []
			rs.append(r)
			newNode = Node(self.players[player].ip,
							self.players[player].myport, 
							self.height, 
							self.width,
							head,
							random.randint(0, 7),
							rs,
							counter,
							self.players[player].name)
			self.players[player].node = newNode
			if len(nmap) <= i:
				nmap.append([])
			nmap[i].append(newNode)

		i = -1;
		j = 0;
		for player in self.players.keys():
			i = i + 1
			if i == x:
				j = j + 1
				i = 0;
			ns = {}
			if i != 0:
				ns[nmap[i - 1][j].myId] = nmap[i - 1][j]
			if j != 0:
				ns[nmap[i][j - 1].myId] = nmap[i][j - 1]
			if len(nmap) > i + 1 and len(nmap[i + 1]) > j:
				ns[nmap[i + 1][j].myId] = nmap[i + 1][j]
			if len(nmap) > i and len(nmap[i]) > j + 1:
				ns[nmap[i][j + 1].myId] = nmap[i][j + 1]
			self.players[player].node.setNeighbors(ns)

	def getPlayerNames(self):
		return self.players.keys()

	def printPlayer(self):
		for player in self.players.keys():
			print 'name %s : ip %s' % (self.players[player].getName(), self.players[player].getIp())

class Server(threading.Thread):
	storage = None

	def getMsg(self):
		return self.storage

	def popMsg(self):
		self.storage = None
	
	def __init__(self, ip, port, choice):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.creator = choice

	def run ( self ):
		print 'server run:'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.ip, self.port))
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
			print 'string', client_resp
			recv_msg = pickle.loads(client_resp)	
			peerlist = recv_msg.peerlist
			print 'List : '
			self.storage = recv_msg
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
	
class client(threading.Thread):
    
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.port = port
        self.ip = ip # Get local machine name
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
    def run(self):
        print 'Connecting to ', self.ip, self.port
        self.clientSock.connect((self.ip, self.port))  
        
    def send(self, data):
    	print 'data'
    	print data.name
    	print data.ip
    	print data.port 
    	print data.data
    	print data.msg_type      
        send_data  = pickle.dumps(data)
        self.clientSock.send(send_data)

