import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np

class Queens8:

	def __init__(self):
		# create master tkinter window
		self.root = tk.Tk()

		self.window_height = 420
		self.window_width = 400

		self.array = np.full((8,8),0)		
		self.tdelta = 30
		
		self.init_window()
		
	def init_window(self):
		# window properties
		self.root.wm_title("Sudoku Solver")
		self.root.wm_minsize(width=self.window_width, height=self.window_height)
		self.root.wm_resizable(width=False, height=False)
		
		# gui frame
		self.top_frame = tk.Frame(self.root)
		self.top_frame.grid(row=0, sticky='w')
		
		# solve button
		self.solve_button = ttk.Button(self.top_frame, text="Solve", command=self.solve)
		self.solve_button.grid(row=0, column=1, sticky='w')
		
		# create canvas to display images, and array to hold drawn objects
		self.canvas = tk.Canvas(self.root)
		self.grid_lines = []
		self.queens = []
		
		self.blip_canvas()


	def draw_canvas(self): #draws the canvas
		h = self.window_height-20
		w = self.window_width
		self.canvas = tk.Canvas(self.root, width=w, height=h)
		self.canvas.grid(row=1)

		#draw grid
		self.grid_lines = []
		for i in range(0,w,50):
			self.grid_lines.append(self.canvas.create_line(i,0,i,h))
		for j in range(0,h,50):
			self.grid_lines.append(self.canvas.create_line(0,j,w,j))

		#fill in grid
		self.queens = []

		icon = Image.open("queen.jpg")
		icon = icon.resize((50,50), resample = 0)
		self.canvas.image = ImageTk.PhotoImage(icon)
		
		#draw queens
		for i in range(0,8):
			for j in range(0,8):
				if self.array[i][j] == 1:
					self.queens.append(self.canvas.create_image(j*50+25,i*50+25,image = self.canvas.image))
		
			
		

	def blip_canvas(self): #updates the canvas
		self.canvas.delete(self.queens)
		self.draw_canvas() # redraw canvas 
		self.root.update() # update window
		self.root.after(self.tdelta) #wait before next update
		
	
	def solve(self):
		print(self.solve_queens(0))
		for i in range(0,8):
			print(self.array[i])
		
	
	def solve_queens(self, row):
		if row == 8: #no more rows, done
			return 1
		
		for col in range (0,8): #try putting in 1-8 columns
			if self.check_conflicts(col,row) == 0: #if assignment is valid
				self.array[col][row] = 1 #try assignment	
				self.blip_canvas()
				
				if (self.solve_queens(row+1) == 1):
					return 1# if recursive calls succeeds in solving
				
				self.array[col][row] = 0 # if not valid reset it
		return 0
			
		
	
	def check_conflicts(self, col, row):
		for i in range (len(self.array[0])): #check if duplicates in row
			if self.array[i][row] == 1:
				return 1
				
		for j in range(len(self.array)): #check if duplicates in column
			if self.array[col][j] == 1:
				return 1

		for k in range (len(self.array)): #check if duplicates in diagonal going forward
			i = (col+k)%8
			j = (row+k)%8
			
			if col+k >= 8 and row+k >= 8 or col+k < 8 and row+k < 8:
				if self.array[i][j] == 1:
					return 1
			
		
		for k in range (len(self.array)): #check if duplicates in diagonal going backward
			i = (col+k)%8
			j = (row-k)%8	
			
			if col+k >= 8 and row-k < 0 or col+k < 8 and row-k >= 0:
				if self.array[i][j] == 1:
					return 1
				
		return 0
			
			
			
	
	def start(self):
		tk.mainloop()
		
if __name__ == '__main__':
	
	app = Queens8()
	app.start()