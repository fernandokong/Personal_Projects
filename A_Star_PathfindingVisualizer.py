import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import math

class Node:
	def __init__(self, x, y, h, g, parent):
		self.x = x # x position
		self.y = y # y position
		self.parent = parent # parent node
		self.f = h+g # manhattan distance + num of moves to reach current square
		self.h = h # manhattan distance
		self.g = g # num of moves to reach current square

class PathfindingVisualizer:

	def __init__(self):
		# create master tkinter window
		self.root = tk.Tk()

		self.window_height = 720
		self.window_width = 1200		
		self.tdelta = 10
		self.array = np.full((48,28),0)			
		self.drawing_allowed = 1
		
		self.init_window()
		
	def init_window(self):
		# window properties
		self.root.wm_title("A* Pathfinding Visualizer")
		self.root.wm_minsize(width=self.window_width, height=self.window_height)
		self.root.wm_resizable(width=False, height=False)
		
		# gui frame
		self.top_frame = tk.Frame(self.root)
		self.top_frame.grid(row=0, sticky='w')
		
		# solve button
		self.solve_button = ttk.Button(self.top_frame, text="Solve", command=self.solve)
		self.solve_button.grid(row=0, column=0, sticky='w')
		
		# clear grid button
		self.clear_button = ttk.Button(self.top_frame, text="Clear Grid", command=self.init_grid)
		self.clear_button.grid(row=0, column=1, sticky='w')
				
		# create canvas to display images, and array to hold drawn objects
		self.canvas = tk.Canvas(self.root)
		self.grid_lines = []
		self.points = []
		
		# initialize the map
		self.init_grid()
		
		# update canvas
		self.blip_canvas()

	def init_grid(self): #clear grid and set start and end positions to default
		drawing_allowed = 0
		self.array = np.full((48,28),0)
		self.array[0][0] = 1
		self.array[47][27] = 2
		self.blip_canvas()
		
		drawing_allowed = 1
		self.draw_type = 3


	def click(self, event):
		if self.drawing_allowed == 1:
			try:
				x = event.x/25
				y = event.y/25
				#import pdb; pdb.set_trace()
				if self.array[x][y] == 0: #don't overwrite blocks that already have values
					if x < 3 and y < 3 or x > 44 and y > 24: #create a no wall zone around start and end 
						pass
					else:
						self.array[x][y] = 3
				self.blip_canvas()
			except:
				pass	

	def motion(self, event):
		label_mouse1 = "Mouse position"
		self.label_m1 = tk.Label(self.top_frame, text=label_mouse1)
		self.label_m1.grid(row=1, column = 0)
		
		label_mouse2 = str("(X: %s Y: %s)" % (event.x, event.y))
		self.label_m2 = tk.Label(self.top_frame, text=label_mouse2)
		self.label_m2.grid(row=1, column = 1)

	def draw_canvas(self): #draws the canvas
		h = self.window_height-20
		w = self.window_width
		self.canvas = tk.Canvas(self.root, width=w, height=h)
		self.canvas.grid(row=2)
		
		self.root.bind("<Motion>", self.motion)
		self.root.bind("<B1-Motion>", self.click)
		
		gridsize = 25

		#fill in grid
		self.points = []
		
		#draw points
		for i in range(48):
			for j in range(28):
				if self.array[i][j] == 1: #start
					self.points.append(self.canvas.create_rectangle(i*gridsize,j*gridsize,(i+1)*gridsize, (j+1)*gridsize,fill = 'green'))
				elif self.array[i][j] == 2: #target
					self.points.append(self.canvas.create_rectangle(i*gridsize,j*gridsize,(i+1)*gridsize, (j+1)*gridsize,fill = 'red'))
				elif self.array[i][j] == 3: #blocks
					self.points.append(self.canvas.create_rectangle(i*gridsize,j*gridsize,(i+1)*gridsize, (j+1)*gridsize,fill = 'black'))
				elif self.array[i][j] == 4: #open list
					self.points.append(self.canvas.create_rectangle(i*gridsize,j*gridsize,(i+1)*gridsize, (j+1)*gridsize,fill = 'yellow'))
				elif self.array[i][j] == 5: #closed list
					self.points.append(self.canvas.create_rectangle(i*gridsize,j*gridsize,(i+1)*gridsize, (j+1)*gridsize,fill = 'orange'))
				elif self.array[i][j] == 6: #closed list
					self.points.append(self.canvas.create_rectangle(i*gridsize,j*gridsize,(i+1)*gridsize, (j+1)*gridsize,fill = 'blue'))
				
		#draw grid
		self.grid_lines = []
		for i in range(0,w,gridsize):
			self.grid_lines.append(self.canvas.create_line(i,0,i,h))
		for j in range(0,h,gridsize):
			self.grid_lines.append(self.canvas.create_line(0,j,w,j))

		
	def blip_canvas(self): #updates the canvas
		self.canvas.delete(self.points)
		self.draw_canvas() # redraw canvas 
		self.root.update() # update window
		self.root.after(self.tdelta) #wait before next update
		
	
	def solve(self):
		self.drawing_allowed = 0
		map_list = self.array.copy() #want to keep the map used in algorithm and the drawn map separate
		map_list[47][27] = 0 #set end to 0 so its not considered a wall
		self.a_star_solve(map_list,47,27, 0,0)
		self.drawing_allowed = 1
		
	
	def is_finished(self, closed_list, end_x, end_y):
		for index_node in closed_list:
			if index_node.x == end_x and index_node.y == end_y:
				return index_node
		return None
		
	def is_in_closed_list(self, closed_list, node): #check if an element is in closed list by comparing positions
		for i in range(len(closed_list)):
			index_node = closed_list[i]
			if index_node.x == node.x and index_node.y == node.y:
				return i #return node position
		return -1 #node not in list	

	def is_in_open_list(self, open_list, node): #check if an element is in open list by comparing positions 
		for i in range(len(open_list)):
			index_node = open_list[i]
			if index_node.x == node.x and index_node.y == node.y:
				if index_node.g > node.g: # if we can get to this node in less moves, change the parent node
					index_node.parent = node.parent
				return i #return node position
		return -1 #node not in list

	def find_lowest(self, open_list): #returns lowest open list node
		lowest = open_list[0]
		for node in open_list:
			if node.f < lowest.f:
				lowest = node
		return lowest
			

	def is_wall(self, map_list, node):
		try:
			if node.x > -1 and node.y > -1:
				return map_list[node.x][node.y]
		except: #array out of bounds
			pass
		return 1 #treat out of bounds as walls
				
	def open_to_closed(self, open_list, closed_list, node):
		index = self.is_in_open_list(open_list, node)
		try:
			self.array[node.x][node.y] = 5
			closed_list.append(open_list.pop(index))
			self.blip_canvas()
		except:
			pass #element not in open list

	def manhattan(self, end_x, end_y, x, y): #return shortest distance between two points
		return abs(end_x-x)+abs(end_y-y)

	# checks if diagonal is valid, don't want to traverse diagonally through gap in the wall
	# want to avoid this situation, where the path travels through a diagonal wall
	# 00010
	# **100
	# 01***
	# 01000
	# 1-wall, 0-empty space, *-path
	def check_diag(self, map_list, node): 
		if map_list[node.x][node.parent.y] == 0 or map_list[node.parent.x][node.y] == 0:
			return 1 #valid path
		return 0

	def create_node(self, open_list, closed_list, map_list, end_x, end_y, x, y, g, parent, diag): #creates a new node that is appended to the open list if it satisfies some conditions
		new_node = Node(x, y, self.manhattan(end_x, end_y, x, y), g, parent)
		if self.is_wall(map_list, new_node) == 0: #if not a wall, add to open list
			if diag == 0 or self.check_diag(map_list, new_node) == 1: #check if diagonal and then check if it goes through diagonal walls
				if self.is_in_open_list(open_list, new_node) == -1 and self.is_in_closed_list(closed_list, new_node) == -1: #if not in open list or closed list
					open_list.append(new_node)
					self.array[new_node.x][new_node.y] = 4
					self.blip_canvas()
					
					

	def a_star_solve(self, map_list, end_x, end_y, start_x, start_y):	
		open_list = []
		closed_list = []
		open_list.append(Node(start_x, start_y, self.manhattan(end_x, end_y, start_x, start_y), 0, None))
		
		end_node = None
				
		while len(open_list) > 0:
		
			curr_node = self.find_lowest(open_list) #set lowest f-value node as the current node
			self.open_to_closed(open_list, closed_list, curr_node) #send current node to closed list
						
			end_node = self.is_finished(closed_list, end_x, end_y)
			if end_node is not None: #check if we are finished
				break
			
			#find scores for cardinal directions and adds it to open list if not in a wall, current node is the parent
			g = curr_node.g + 1
			x = curr_node.x
			y = curr_node.y
			
			
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x, y-1, g, curr_node, 0) #above tile
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x, y+1, g, curr_node, 0) #below tile
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x+1, y, g, curr_node, 0) #right tile
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x-1, y, g, curr_node, 0) #left tile
			
			#find scores for diagonals and adds it to open list, current node is the parent
			g = curr_node.g + math.sqrt(2) # diagonal distance
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x-1, y-1, g, curr_node, 1) #top-left tile
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x+1, y-1, g, curr_node, 1) #top-right tile
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x-1, y+1, g, curr_node, 1) #bottom-left tile
			self.create_node(open_list, closed_list, map_list, end_x, end_y, x+1, y+1, g, curr_node, 1) #bottom-right tile
			
			
			
		if end_node is not None:
			node = end_node
			while node is not None:
				self.array[node.x][node.y] = 2
				self.blip_canvas()
				node = node.parent
			
			
	
	def start(self):
		tk.mainloop()
		
if __name__ == '__main__':
	
	app = PathfindingVisualizer()
	app.start()