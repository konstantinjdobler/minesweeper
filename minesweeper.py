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
CORRECT_FLAGS = 0
gui_field_list = [[None] * FIELD_WIDTH for i in range(FIELD_HEIGHT)]
field_list = [[None] * FIELD_WIDTH for i in range(FIELD_HEIGHT)]

def iterate_over_neighbours(condition, action):
	for j in range(-1, 2):
		for i in range(-1, 2):
			if x+i >= 0 and y+j >=0:
				try:
					if field_list[y+j][x+i].is_bomb() == True: 
						counter +=1
				except: IndexError

def set_bombs():
	for _ in range(BOMB_COUNT):
		random_y = random.randint(0,FIELD_HEIGHT-1)
		random_x = random.randint(0,FIELD_WIDTH-1)
		while field_list[random_y][random_x].is_bomb() == True:
			random_y = random.randint(0,FIELD_HEIGHT-1)
			random_x = random.randint(0,FIELD_WIDTH-1)
		field_list[random_y][random_x].set_bomb_status(True)

def set_field_values():
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			field_list[y][x].set_value(count_neighbour_bombs(x,y))   

def count_neighbour_bombs(x, y):
	counter = 0
	for j in range(-1, 2):
		for i in range(-1, 2):
				try:
					if field_list[y+j][x+i].is_bomb() == True: 
						counter +=1
				except: IndexError
	return counter

def count_flagged_neighbours(x, y):
	counter = 0
	for j in range(-1, 2):
		for i in range(-1, 2):
				try:
					if field_list[y+j][x+i].is_flagged() == True: 
						counter +=1
				except: IndexError
	return counter

def count_hidden_neighbours(x, y):
	counter = 0
	for j in range(-1, 2):
		for i in range(-1, 2):
				try:
					if field_list[y+j][x+i].is_hidden() == True: 
						counter +=1
				except: IndexError
	return counter

def click_hidden_neighbours(x,y):
	for j in range(-1, 2):
		for i in range(-1, 2):
			if x+i >= 0 and y+j >=0:
				try:
					if field_list[y+j][x+i].is_flagged() != True and field_list[y+j][x+i].is_hidden() == True:
						click_field(x+i,y+j,False)
				except: IndexError

def clear_zeros(x,y):
	for j in range(-1, 2):
		for i in range(-1, 2):
			if (j!=0 or i!=0) and x+i >= 0 and y+j >=0:
				try:
					if field_list[y+j][x+i].get_value() == 0 and field_list[y+j][x+i].is_hidden(): 
						field_list[y+j][x+i].set_hidden_status(False)
						clear_zeros(x+i, y+j)
					field_list[y+j][x+i].set_hidden_status(False)
				except: IndexError

def click_field(x, y, update=True):
	field_list[y][x].set_hidden_status(False)   
	if field_list[y][x].get_value() == 0: clear_zeros(x,y)
	if update: update_fields()
	if field_list[y][x].is_bomb(): 
		game_over()

def flag_field(event,x,y,hard_set=False):
	global CORRECT_FLAGS
	if not OVER: 
		if field_list[y][x].is_bomb() and not field_list[y][x].is_flagged():
			CORRECT_FLAGS += 1
		elif field_list[y][x].is_bomb() and field_list[y][x].is_flagged() and not hard_set:
			CORRECT_FLAGS -= 1

		field_list[y][x].set_flag_status((not field_list[y][x].is_flagged()) or hard_set)
		
		if not hard_set: update_fields()
		if CORRECT_FLAGS == BOMB_COUNT: win_game()

def auto_flag(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			if field_list[y][x].get_value() == 1 and field_list[y][x].is_hidden() == False:
				if count_hidden_neighbours(x,y) == 1:
					flag_hidden_neighbours(x,y)

	update_fields()

def flag_hidden_neighbours(x,y):
	for j in range(-1, 2):
		for i in range(-1, 2):
			try:
				if field_list[y+j][x+i].is_hidden() == True:
					flag_field(None, x+i,y+j,True)
			except: IndexError

def auto_flag_all(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
				hidden_neighbours = count_hidden_neighbours(x,y) 
				if field_list[y][x].get_value() == hidden_neighbours and field_list[y][x].is_hidden() == False:
					flag_hidden_neighbours(x,y)
	update_fields()

def click_obvious(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			if field_list[y][x].get_value()==1 and field_list[y][x].is_hidden() == False:
				if count_flagged_neighbours(x,y) is 1:
					click_hidden_neighbours(x,y)
	update_fields()

def click_all(event = None):
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
				if count_flagged_neighbours(x,y) is field_list[y][x].get_value() and field_list[y][x].is_hidden() == False:
					click_hidden_neighbours(x,y)
	update_fields()

def game_over():
	global OVER 
	OVER = True
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			gui_field_list[y][x].configure(state=DISABLED)
	messagebox.showerror("Game Lost!", "You hit a bomb!")

def win_game():
	global OVER 
	OVER = True
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			gui_field_list[y][x].configure(state=DISABLED)
	messagebox.showinfo("Game Won!", "You are very smart!")

def update_fields():
	for y in range (0,FIELD_HEIGHT):
		for x in range(0,FIELD_WIDTH):
			if field_list[y][x].is_hidden() == False:
				if field_list[y][x].is_bomb(): gui_field_list[y][x].configure(text = "B", state = DISABLED, bg = "light grey", disabledforeground = "orange")
				elif field_list[y][x].value == 0: gui_field_list[y][x].configure(text = str(field_list[y][x].value), bg = "light grey", state = DISABLED, disabledforeground = "light blue")
				elif field_list[y][x].value == 1: gui_field_list[y][x].configure(text = str(field_list[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "dark blue")
				elif field_list[y][x].value == 2: gui_field_list[y][x].configure(text = str(field_list[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "green")
				elif field_list[y][x].value == 3: gui_field_list[y][x].configure(text = str(field_list[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "red")
				elif field_list[y][x].value == 4: gui_field_list[y][x].configure(text = str(field_list[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "yellow")
				elif field_list[y][x].value >= 5: gui_field_list[y][x].configure(text = str(field_list[y][x].value), bg = "light grey",state = DISABLED, disabledforeground = "black")
			elif field_list[y][x].is_flagged(): 
				gui_field_list[y][x].configure(bg = "violet")
			else: gui_field_list[y][x].configure(bg = "grey")

def quit():
    root.destroy()
##################### function declarations over ##################################

root = Tk()
geometrystring = str(FIELD_SIZE*FIELD_WIDTH)+"x"+str(FIELD_SIZE*FIELD_HEIGHT)
root.geometry(geometrystring)
root.resizable(width=False, height=False)

root.bind("<space>", auto_flag)
root.bind("<c>", click_obvious)
root.bind("<a>", click_all)
root.bind("<f>", auto_flag_all)
for y in range (0,FIELD_HEIGHT):
	for x in range(0,FIELD_WIDTH):
		field_list[y][x] = Field(x,y)
		
		
set_bombs()
set_field_values()
for y in range (0,FIELD_HEIGHT):
	for x in range(0,FIELD_WIDTH):
		gui_field_list[y][x] = Button(root, bg = "grey", command = lambda y1=y, x1=x: click_field(x1,y1), relief = "ridge", font = ("Arial", 20, "bold"))
		gui_field_list[y][x].bind('<Button-3>', lambda event, y1=y, x1=x: flag_field(event,x1,y1,False))
		gui_field_list[y][x].place(height = FIELD_SIZE, width = FIELD_SIZE, x = x*FIELD_SIZE, y = y*FIELD_SIZE)
update_fields()
root.mainloop()
