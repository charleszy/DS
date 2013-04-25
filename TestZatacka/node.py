class Point:
	x = 0
	y = 0

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

class Rectangle:
	tl = None
	br = None
	track = []

class Segment:
	x1 = 0
	x2 = 0
	y = 0
	tag = 0
	value = 0


class Node:
	name = ''
	height = 0
	width = 0
	head = Point()
	direction = 0
	status = None
	counter = 0
	ip = ''
	port = 0
	myId = -1
	stats = {}

	track = []
	rectangles = []
	neighbors = {}
	x = [0, 1, 1, 1, 0, -1, -1, -1]
	y = [1, 1, 0, -1, -1, -1, 0, 1]

	def __init__(self, ip, port, height, width, head, direction, rectangles, myId, name):
		self.width = width
		self.height = height
		self.head = head
		self.direction = direction
		self.rectangles = rectangles
		self.ip = ip
		self.port = port
		self.myId = myId
		self.track.append({'x': head.x, 'y': head.y})
		self.name = name

	def setNeighbors(self, neighbors):
		self.neighbors = neighbors

	def inside(self, head, rect):
		ps = [rect.tl, rect.tl, rect.br, rect.br, rect.tl]
		ps[1].y = rect.br.y
		ps[3].y = rect.tl.y
		x1 = head.x
		y1 = head.y
		for i in range(0, 4):
			x2 = ps[i].x
			y2 = ps[i].y
			x3 = ps[i + 1].x
			y3 = ps[i + 1].y
			s = x1 * y2 - x1 * y3 - x2 * y1 + x3 * y1 + x2 * y3 - x3 * y2
			if s < 0:
				return False
		return True

	def createSeg(self, rectangles):
		print 'createSeg'
		seg = []
		for r in rectangles:
			seg1 = Segment()
			seg1.x1 = r.tl.x
			seg1.x2 = r.br.x
			seg1.y = r.tl.y
			seg1.tag = 1
			seg1.value = 1
			seg.append(seg1)
			print seg1.x1, ' ', seg1.x2, ' ', seg1.y

			seg2 = Segment()
			seg2.x1 = r.tl.x
			seg2.x2 = r.br.x
			seg2.y = r.br.y
			seg2.tag = -1
			seg2.value = 1
			seg.append(seg2)
			print seg2.x1, ' ', seg2.x2, ' ', seg2.y

		for i in range(0, len(seg) - 1):
			for j in range(i + 1, len(seg)):
				if seg[i].y > seg[j].y:
					tmp = seg[i]
					seg[i] = seg[j]
					seg[j] = tmp

		return seg

	def generateRectangles(self, result):
		print 'generateRectangles'
		for i in range(0, len(result) - 1):
			for j in range(i + 1, len(result)):
				if result[i].y > result[j].y:
					tmp = result[i]
					result[i] = result[j]
					result[j] = tmp

		self.rectangles = []
		i = 0
		stack = []
		apd = []
		while i < len(result):
			flag = False
			for j in range(reverse(len(stack))):
				seg = stack[j]
				newRect = Rectangle()
				newRect.tl = Point(seg.x1, seg.y)
				newRect.br = Point(seg.x2, result[i].y - 1)
				self.rectangles.append(newRect)
				print newRect.tl.x, ' ', newRect.tl.y
				print newRect.br.x, ' ', newRect.br.y
				if result[i].tag == -1:
					if seg.x1 < result[i].x1 and seg.x2 > result[i].x2:
						newSeg = Segment()
						newSeg.x1 = result[i].x2
						newSeg.x2 = seg.x2
						newSeg.y = result[i].y
						newSeg.tag = 1
						apd.append(newSeg)
						stack[j].x2 = result[i].x1
					elif seg.x1 == result[i].x1 and seg.x2 == result[i].x2:
						del stack[j]
					elif seg.x1 < result[i].x1 and seg.x2 == result[i].x2:
						stack[j].x2 = result[i].x1 - 1
					elif seg.x1 == result[i].x1 and seg.x2 > result[i].x2:
						stack[j].x1 = result[i].x2 + 1

			stack.append(apd)

			if result[i].tag == 1:
				stack.append(result[i])
			for j in range(0, 2):
				for k in range(reverse(len(stack) - 1)):
					if stack[k].x1 == stack[k + 1].x2:
						stack[k + 1].x2 = stack[k].x2
						del stack[k]
					elif stack[k].x2 == stack[k + 1].x1:
						stack[k].x2 = stack[k + 1].x2
						del stack[k + 1]

			for seg in stack:
				seg.y = result[i].y

	def intersection(self, rectangles):
		print 'intersection'
		seg1 = self.createSeg(self.rectangles)
		seg2 = self.createSeg(n.rectangles)

		result = seg1
		result.append(seg2)

		for i in range(0, len(result) - 1):
			for j in range(i + 1, len(result)):
				if result[i].y > result[j].y:
					tmp = result[i]
					result[i] = result[j]
					result[j] = tmp

		self.rectangles = []
		i = 0
		stack = []
		apd = []
		while i < len(result):
			flag = False
			for j in range(reverse(len(stack))):
				seg = stack[j]
				newRect = Rectangle()
				newRect.tl = Point(seg.x1, seg.y)
				newRect.br = Point(seg.x2, result[i].y - 1)
				self.rectangles.append(newRect)
				print newRect.tl.x, ' ', newRect.tl.y
				print newRect.br.x, ' ', newRect.br.y
				if result[i].tag == -1:
					if seg.x1 < result[i].x1 and seg.x2 > result[i].x2:
						newSeg = Segment()
						newSeg.x1 = result[i].x2
						newSeg.x2 = seg.x2
						newSeg.y = result[i].y
						newSeg.tag = seg.value
						newSeg.value = seg.value
						apd.append(newSeg)
						result[i].value = seg.value - 1
						if result[i].value != 0:
							result[i].tag = 1
							apd.append(result[i])
						stack[j].x2 = result[i].x1
					elif seg.x1 == result[i].x1 and seg.x2 == result[i].x2:
						if seg.value == 1:
							del stack[j]
						else:
							stack[j].value -= 1
					elif seg.x1 < result[i].x1 and seg.x2 == result[i].x2:
						newSeg = Segment()
						newSeg.x1 = seg.x1
						newSeg.x2 = result[i].x1 - 1
						newSeg.y = result[i].y
						newSeg.tag = seg.tag
						newSeg.value = seg.value
						apd.append(newSeg)
						stack[j].x1 = result[i].x1
						stack[j].value -= 1
						if stack[j].value == 0:
							del stack[j]
					elif seg.x1 == result[i].x1 and seg.x2 > result[i].x2:
						stack[j].x1 = result[i].x2

			stack.append(apd)

			if result[i].tag == 1:
				stack.append(result[i])
			for j in range(0, 2):
				for k in range(reverse(len(stack) - 1)):
					if stack[k].x1 == stack[k + 1].x2:
						stack[k + 1].x2 = stack[k].x2
						del stack[k]
					elif stack[k].x2 == stack[k + 1].x1:
						stack[k].x2 = stack[k + 1].x2
						del stack[k + 1]

			for seg in stack:
				seg.y = result[i].y

	def union(self, n):
		print 'union'
		for nId in n.neighbors.keys():
			if nId != self.myId:
				self.neighbors[nId] = n.neighbors[nId]

		seg1 = self.createSeg(self.rectangles, 1)
		seg2 = self.createSeg(n.rectangles, 1)

		result = seg1
		result.append(seg2)

		self.generateRectangles(result)


	def checkNeighbors(self):
		print 'checkNeighbors'
		for nId in self.neighbors.keys():
			n = self.neighbors[nId]
			for k in n.stats.keys():
				self.stats[k] = n.stats[k]
			for nnId in n.neighbors.keys():
				if nnId == self.myId:
					self.intersection(n.neighbors[nnId].rectangles)

    		if n.status != None:
    			if n.status.myId == self.myId:
    				del self.neighbors[nId]
    				self.union(n)
    			else:
    				self.neighbors[nId] = n.status

	def die(self):
		print 'die'
		maxId = -1
		saveN = None
		for nId in self.neighbors.keys():
			if nId > maxId:
				maxId = nId
				saveN = self.neighbors[nId]
		self.status = saveN
		self.stats[(self.ip, self.port)] = self.counter

	def divide(self, rect):
		print 'divide'
		head = self.head

		for p in rect.track:
			if p.x == head.x and p.y == head.y:
				self.die()
				return None
		rect.track.append(head)
		ret = []

		tick = 0
		
		while True:
			tick = tick ^ 1
			if rect.track == None:
				self.rectangles.append(rect)
				return ret

			r = Rectangle()
			r.tl = rect.tl
			r.br = rect.br
			if tick == 1:
				if head.y == rect.tl.y and rect.tl.y != rect.br.y:
					rect.br.y = (rect.br.y + 1) / 2
					r.tl.y = rect.br.y + 1
				elif head.y == rect.br.y and rect.tl.y != rect.br.y:
					r.br.y = (r.br.y + 1) / 2
					rect.tl.y = r.br.y + 1
				elif head.x == rect.tl.x and rect.tl.x != rect.br.x:
					rect.br.x = (rect.br.x + 1) / 2
					r.tl.x = rect.br.x + 1
				else:
					r.br.x = (r.br.x + 1) / 2
					rect.tl.x = r.br.x + 1
			else:
				if head.x == rect.tl.x and rect.tl.x != rect.br.x:
					rect.br.x = (rect.br.x + 1) / 2
					r.tl.x = rect.br.x + 1
				elif head.x == rect.br.x and rect.tl.x != rect.br.x:
					r.br.x = (r.br.x + 1) / 2
					rect.tl.x = r.br.x + 1
				elif head.y == rect.tl.y and rect.tl.y != rect.br.y:
					rect.br.y = (rect.br.y + 1) / 2
					r.tl.y = rect.br.y + 1
				else:
					r.br.y = (r.br.y + 1) / 2
					rect.tl.y = r.br.y + 1
				
			for i in range(reverse(len(rect.track))):
				if self.inside(rect.track[i], r):
					r.track.append(rect.track[i])
					del rect.track[i]
				ret.append(r)

	def rearrange(self):
		print 'rearrange'
		for nId in self.neighbors:
			for i in range(0, len(self.neighbors[nId].rectangles)):
				if self.inside(self.head, self.neighbors[nId].rectangles[i]):
					ret = self.divide(self.neighbors[nId].rectangles[i])
					if ret != None:
						del self.neighbors[nId].rectangles[i]
						self.neighbors[nId].rectangles.append(ret)
					break

	def receive(self, node):
		self.neighbors[node.myId] = node

	def send(self, neighbors, node):
		pass

	def update(self, direction, color):
		print 'update'
		self.counter = self.counter + 1
		self.head.x += Node.x[direction]
		self.head.y += Node.y[direction]

		if self.head.x < 0 or self.head.x >= self.height or self.head.y < 0 or self.head.y >= self.width:
			self.die()

		if color == 1:
			self.track.append({'x': self.head.x, 'y': self.head.y})

		if len(self.neighbors) == 0:
			return 1 #win
		else:
			self.checkNeighbors()

		if self.status == None:
			flag = False
			for r in self.rectangles:
				if self.inside(self.head, r):
					flag = True
					if color == 1:
						r.track.append(self.head)
					break
			if not flag:
				self.rearrange()

		if self.status != None:
			return -1 #lose

		return 0 #continue

	def show(self):
		print 'show'
		print self.name
		print self.head.x, ' ', self.head.y
		for r in self.rectangles:
			print 'tl', r.tl.x, ' ', r.tl.y, ' br', r.br.x, ' ', r.br.y
		print len(self.neighbors)
