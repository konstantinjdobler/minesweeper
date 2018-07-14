class Field:
	hidden = True
	bomb = False
	value = 0
	flagged = False
	def __init__(self, x, y):
		self.x = x
		self.y = y
		

	def setBomb(self, bool):
		self.bomb = bool

	def setFlag(self, bool):
		self.flagged = bool

	def setHidden(self, bool):
		self.hidden = bool

	def setValue(self, i):
		self.value = i

	def isBomb(self):
		return self.bomb 

	def isHidden(self):
		return self.hidden 

	def getValue(self):
		return self.value

	def isFlagged(self):
		return self.flagged
