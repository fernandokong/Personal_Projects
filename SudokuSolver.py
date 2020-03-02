import tkinter as tk
from tkinter import ttk
import math

class SudokuSolver:

	def __init__(self, array):
		# create master tkinter window
		self.root = tk.Tk()

		self.window_height = 470
		self.window_width = 450
		
		self.array = array
		
		self.tdelta = 20
		
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
		self.numbers = []
		
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
			if (i/50)%3 == 0:
				self.grid_lines.append(self.canvas.create_line(i,0,i,h, width = 3))
		for j in range(0,h,50):
			self.grid_lines.append(self.canvas.create_line(0,j,w,j))
			if (j/50)%3 == 0:
				self.grid_lines.append(self.canvas.create_line(0,j,w,j, width = 3))

		#fill in grid
		self.numbers = []
		for i in range(0,9):
			for j in range(0,9):
				num = str(self.array[i][j])
				self.numbers.append(self.canvas.create_text(j*50+25,i*50+25,fill="darkblue",font="Times 20 bold", text = num))
		
			
		

	def blip_canvas(self): #updates the canvas
		self.canvas.delete(self.numbers)# clear current numbers
		self.draw_canvas() # redraw canvas 
		self.root.update() # update window
		self.root.after(self.tdelta) #wait before next update
		
	
	def solve(self):
		print(self.solve_sudoku())
		for i in range(0,9):
			print(self.array[i])
		
	
	def solve_sudoku(self):
		i,j = self.next_zero()
		if i == -1 or j == -1: #no more zeroes, done
			return 1
		
		for num in range (1,10): #try putting in 1-9
			if self.check_conflicts(i,j, num) == 0: #if assignment is valid
				self.array[i][j] = num #try assignment
				self.blip_canvas()
				
				if (self.solve_sudoku() == 1):
					return 1# if recursive calls succeeds in solving
				
				self.array[i][j] = 0 # if not valid reset it
		return 0
			
		
		
	def next_zero(self):
		for i in range(0, len(self.array)): #iterate row
			for j in range(0, len(self.array[0])): #iterate col
				if self.array[i][j] == 0:
					return i,j
		return -1,-1
				
	
	def check_conflicts(self, col, row, num):
		for i in range (len(self.array[0])): #check if duplicates in row
			if self.array[i][row] == num:
				return 1
				
		for j in range(len(self.array)): #check if duplicates in column
			if self.array[col][j] == num:
				return 1
		
		sq_col, sq_row = (col/3)*3, (row/3)*3
		
		for i in range (sq_col, sq_col+3): #check if duplicates in square
			for j in range (sq_row, sq_row+3):
				if self.array[i][j] == num:
					return 1
				
		return 0
			
			
			
	
	def start(self):
		tk.mainloop()
		
if __name__ == '__main__':
	
	# Array is [yPos][xPos]
	testArray = [[3,0,6,5,0,8,4,0,0],
				[5,2,0,0,0,0,0,0,0],
				[0,8,7,0,0,0,0,3,1],
				[0,0,3,0,1,0,0,8,0],
				[9,0,0,8,6,3,0,0,5],
				[0,5,0,0,9,0,6,0,0],
				[1,3,0,0,0,0,2,5,0],
				[0,0,0,0,0,0,0,7,4],
				[0,0,5,2,0,6,3,0,0]]

	app = SudokuSolver(testArray)
	app.start()