class Field:
	hidden: bool = True
	bomb: bool = False
	value: int = 0
	flagged: bool = False
	def __init__(self, x, y):
		self.x = x
		self.y = y
		

	def set_bomb_status(self, state: bool):
		self.bomb = state

	def set_flag_status(self, state: bool):
		self.flagged = state

	def set_hidden_status(self, state: bool):
		self.hidden = state

	def set_value(self, value: int):
		self.value = value

	def is_bomb(self):
		return self.bomb 

	def is_hidden(self):
		return self.hidden 

	def get_value(self):
		return self.value

	def is_flagged(self):
		return self.flagged
