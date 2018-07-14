from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random
from field_class import *

OVER = False
BOMB_COUNT = 110
FIELD_HEIGHT = 20
FIELD_WIDTH = 30
FIELD_SIZE = 30
RIGHT_FLAGS = 0
list = [[None] * FIELD_WIDTH for i in range(FIELD_HEIGHT)]
flist = [[None] * FIELD_WIDTH for i in range(FIELD_HEIGHT)]



def setBombs():
	for x in range(BOMB_COUNT):
		randy = random.randint(0,FIELD_HEIGHT-1)
		randx = random.randint(0,FIELD_WIDTH-1)
		while flist[randy][randx].isBomb() == True:
			randy = random.randint(0,FIELD_HEIGHT-1)
			randx = random.randint(0,FIELD_WIDTH-1)
		flist[randy][randx].setBomb(True)

def setFieldValues():
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			flist[y][x].setValue(countNeighborBombs(x,y))   

def countNeighborBombs(x, y):
	counter = 0
	for j in range(-1, 2):
		for i in range(-1, 2):
			if x+i >= 0 and y+j >=0:
				try:
					if flist[y+j][x+i].isBomb() == True: 
						counter +=1
				except: IndexError
	return counter

def countNeighborFlagged(x, y):
	counter = 0
	for j in range(-1, 2):
		for i in range(-1, 2):
			if x+i >= 0 and y+j >=0:
				try:
					if flist[y+j][x+i].isFlagged() == True: 
						counter +=1
				except: IndexError
	return counter

def countNeighborHidden(x, y):
	counter = 0
	
	for j in range(-1, 2):
		for i in range(-1, 2):
			#if x+i >= 0 and y+j >=0:
				try:
					if flist[y+j][x+i].isHidden() == True: 
						counter +=1
						
				except: IndexError
	return counter

def clickAllNeighbors(x,y):
	for j in range(-1, 2):
		for i in range(-1, 2):
			if x+i >= 0 and y+j >=0:
				try:
					if flist[y+j][x+i].isFlagged() != True and flist[y+j][x+i].isHidden() == True:
						clicked(x+i,y+j,False)
				except: IndexError

def loseGame():
	global OVER 
	OVER = True
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			list[y][x].configure(state=DISABLED)
	messagebox.showerror("Game Lost!", "You hit a bomb!")

def winGame():
	global OVER 
	OVER = True
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			list[y][x].configure(state=DISABLED)
	messagebox.showinfo("Game Won!", "You are very smart!")

def clearZeros(x,y):
	for j in range(-1, 2):
		for i in range(-1, 2):
			if (j!=0 or i!=0) and x+i >= 0 and y+j >=0:
				try:
					
					if flist[y+j][x+i].getValue() == 0 and flist[y+j][x+i].isHidden(): 
						flist[y+j][x+i].setHidden(False)
						clearZeros(x+i, y+j)
					flist[y+j][x+i].setHidden(False)
				except: IndexError

def updateFields():
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			if flist[y][x].isHidden() == False:
				if flist[y][x].isBomb(): list[y][x].configure(text = "B", state = DISABLED, bg = "light grey",disabledforeground = "orange")
				elif flist[y][x].value == 0: list[y][x].configure(text = str(flist[y][x].value), bg = "light grey", state = DISABLED, disabledforeground = "light blue")
				elif flist[y][x].value == 1: list[y][x].configure(text = str(flist[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "dark blue")
				elif flist[y][x].value == 2: list[y][x].configure(text = str(flist[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "green")
				elif flist[y][x].value == 3: list[y][x].configure(text = str(flist[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "red")
				elif flist[y][x].value == 4: list[y][x].configure(text = str(flist[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "yellow")
				elif flist[y][x].value >= 5: list[y][x].configure(text = str(flist[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "black")
			elif flist[y][x].isFlagged(): list[y][x].configure(bg = "violet")
			else: list[y][x].configure(bg = "grey")

def clicked(x, y, update=True):
	flist[y][x].setHidden(False)   
	if flist[y][x].getValue() == 0: clearZeros(x,y)
	if update: updateFields()
	if flist[y][x].isBomb(): 
		loseGame()

def flagged(event,x,y,hard_set=False):
	global RIGHT_FLAGS
	if not OVER: 
		if flist[y][x].isBomb() and not flist[y][x].isFlagged():
			RIGHT_FLAGS += 1
		elif flist[y][x].isBomb() and flist[y][x].isFlagged() and not hard_set:
			RIGHT_FLAGS -= 1

		flist[y][x].setFlag((not flist[y][x].isFlagged()) or hard_set)
		
		if not hard_set: updateFields()
		if RIGHT_FLAGS == BOMB_COUNT: winGame()

def autoFlag(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			if flist[y][x].getValue() == 1 and flist[y][x].isHidden() == False:
				if countNeighborHidden(x,y) == 1:
					flagHiddenNeighbors(x,y)

	updateFields()

def flagHiddenNeighbors(x,y):
	for j in range(-1, 2):
		for i in range(-1, 2):
			try:
				if flist[y+j][x+i].isHidden() == True:
					flagged(None, x+i,y+j,True)
			except: IndexError

def autoFlagAll(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
				tupel = countNeighborHidden(x,y) 
				if flist[y][x].getValue()== tupel and flist[y][x].isHidden() == False:
					flagHiddenNeighbors(x,y)

	updateFields()

def clickObvious(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			if flist[y][x].getValue()==1 and flist[y][x].isHidden() == False:
				if countNeighborFlagged(x,y) is 1:
					clickAllNeighbors(x,y)
	updateFields()

def clickAll(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
				if countNeighborFlagged(x,y) is flist[y][x].getValue() and flist[y][x].isHidden() == False:
					clickAllNeighbors(x,y)
	updateFields()




##################### function declarations over ##################################

root = Tk()
geometrystring = str(FIELD_SIZE*FIELD_WIDTH)+"x"+str(FIELD_SIZE*FIELD_HEIGHT)
root.geometry(geometrystring)
root.resizable(width=False, height=False)

root.bind("<space>", autoFlag)
root.bind("<c>", clickObvious)
root.bind("<a>", clickAll)
root.bind("<f>", autoFlagAll)
for y in range (0,FIELD_HEIGHT):
	for x in range(0,FIELD_WIDTH):
		flist[y][x] = Field(x,y)
		
		
setBombs()
setFieldValues()
for y in range (0,FIELD_HEIGHT):
	for x in range(0,FIELD_WIDTH):
		list[y][x] = Button(root, bg = "grey", command = lambda y1=y, x1=x: clicked(x1,y1), relief = "ridge", font = ("Arial", 20, "bold"))
		list[y][x].bind('<Button-3>', lambda event, y1=y, x1=x: flagged(event,x1,y1,False))
		list[y][x].place(height = FIELD_SIZE, width = FIELD_SIZE, x = x*FIELD_SIZE, y = y*FIELD_SIZE)
updateFields()
root.mainloop()
