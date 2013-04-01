class Player:
	name = ''
	ip = ''
	status = ''
	startX = 0
	startY = 0

	def __init__(self, name = '', ip = ''):
		self.name = name
		self.ip = ip
		self.status = 'waiting'

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

class Server:
	tables = {}

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

p1 = Player()
p2 = Player()
p1.setName('CharlesZY')
p1.setIp('192.168.1.1')
p2.setName('CocoDuan')
p2.setIp('192.168.0.1')
t = Table('table1', p1)
t.printPlayer();
t.addPlayer(p2)
t.printPlayer();
s = Server()
s.addTable(t)
for tn in s.getTableNames():
	print tn
	tb = s.getTable(tn)
	tb.printPlayer()

