import tkinter as tk
from tkinter import ttk
import random
import math

class SortingVisualizer:

	def __init__(self):
		# create master tkinter window
		self.root = tk.Tk()
		
		self.window_height = 720
		self.window_width = 1280
		
		self.tdelta = 10
		self.array_size = 50
		self.bar_max_height = 500
		self.bar_width = int(math.floor(50/float(self.array_size)*16))
		self.bar_gap = int(math.floor(50/float(self.array_size)*8))
				
		self.init_window()

		

	def init_window(self):
		# window properties
		self.root.wm_title("Sorting Visualizer")
		self.root.wm_minsize(width=self.window_width, height=self.window_height)
		self.root.wm_resizable(width=False, height=False)

		# gui frame
		self.top_frame = tk.Frame(self.root)
		self.top_frame.grid(row=0, sticky='w')
		
		# create dropdown box
		self.sort_options = ['Select Algorithm', 'Bubble Sort', 'Insertion Sort', 'Selection Sort', 'Quick Sort', 'Merge Sort', 'Heap Sort']
		self.option_var = tk.StringVar()
		self.option_drop = ttk.OptionMenu(self.top_frame, self.option_var, *self.sort_options)
		self.option_drop.config(width=15)
		self.option_drop.grid(row=0, column=1, sticky='ew')

		# sort button
		self.sort_button = ttk.Button(self.top_frame, text="Sort", command=self.choose_sort)
		self.sort_button.grid(row=0, column=2, sticky='w')

		# generate array button
		self.gen_button = ttk.Button(self.top_frame, text="Generate New Array", command=self.new_array)
		self.gen_button.grid(row=0, column=0)
		
		# create canvas to display images, and array to hold drawn bars
		self.sort_canvas = tk.Canvas(self.root)
		self.bars = []

	def new_array(self): # generates new array, and then updates canvas
		self.generate_array()
		self.blip_canvas()

	def generate_array(self): # generates array of random numbers
		self.array = []
		self.num_operations = 0
		self.num_swaps = 0
		i = 0
		while i < self.array_size:
			height = random.randrange(0, self.bar_max_height, 1)
			self.array.append(height)
			i = i + 1

	def draw_canvas(self): #draws the canvas
		label_ops = "Number of Operations: " + str(self.num_operations)
		self.num_label_ops = tk.Label(self.top_frame, text=label_ops)
		self.num_label_ops.grid(row=1)
		
		label_swaps = "Number of Swaps: " + str(self.num_swaps)
		self.num_label_swaps = tk.Label(self.top_frame, text=label_swaps)
		self.num_label_swaps.grid(row=2)

		self.sort_canvas = tk.Canvas(self.root, width=1280, height=600)
		self.sort_canvas.grid(row=1)
		self.sort_canvas.create_line(15, 575, 1265, 575)

		next_bar_pos = self.bar_width + self.bar_gap
		bar_height_multi = int(float(self.window_height-100)/self.bar_max_height)
		
		start_x = 30
		start_y = 575
		self.bars = []
		
		#draw bars
		for bar_height in self.array:
			x1 = start_x + self.bar_width
			y1 = start_y - math.floor(bar_height*bar_height_multi)
			self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1, fill='green'))
			start_x = start_x + next_bar_pos

	def blip_canvas(self): #updates the canvas
		self.sort_canvas.delete(self.bars) #delete all drawn bars
		self.draw_canvas() #redraw bars
		self.root.update() 
		self.root.after(self.tdelta) #wait before next update
	
	def choose_sort(self): #start sort corresponding to dropdown choice
		choice = self.option_var.get()
		if choice == "Bubble Sort":
			self.bubble_sort()
		elif choice == "Insertion Sort":
			self.insertion_sort()
		elif choice == "Selection Sort":
			self.selection_sort()
		elif choice == "Quick Sort":
			self.quick_sort(0, len(self.array)-1)
		elif choice == "Merge Sort":
			self.merge_sort(0, len(self.array)-1)
		elif choice == "Heap Sort":
			self.heap_sort(len(self.array))
		
	
	def bubble_sort(self): # bubble sort, O(n^2)
		n = len(self.array)
		for i in range(n):
			for j in range(n-i-1):
				if self.array[j] > self.array[j+1]:
					self.swap(j,j+1)
					self.num_operations += 1
					

	def insertion_sort(self): # insertion sort, O(n^2)
		n = len(self.array)
		for i in range(1,n,1):
			j = i-1 # leftmost pos
			while self.array[j] > self.array[j+1] and j >= 0:
				self.swap(j, j+1)
				self.num_operations += 1
				j -= 1
			
	def selection_sort(self): # selection sort, O(n^2)
		n = len(self.array)
		for i in range (0,n,1):
			minPos = i
			for j in range(i,n,1):
				if self.array[minPos] > self.array[j]:
					minPos = j
				self.num_operations += 1
			self.swap(i, minPos)
			
	
	def quick_sort(self, low, high): # quick sort, O(nlogn)
		if low < high:
			pivotPos = self.partition(low ,high)
			self.quick_sort(low, pivotPos-1) # recursive call to perform q-sort on unsorted smaller elements list
			self.quick_sort(pivotPos+1, high) # recursive call to perform q-sort on unsorted larger elements list
	
	# builds array of elements smaller than pivot to the left of the pivot and leaves elements larger than pivot to the right of the pivot
	# returns new pivot position
	def partition (self, low, high): 
		pivot = self.array[high]
		i = low # index of last element smaller than pivot
		for j in range (low, high):
			if (self.array[j] < pivot):
				self.swap(i, j)
				i += 1
			self.num_operations += 1
		self.swap(i, high) #swap new pivot position with old pivot position
		return i

	def merge_sort(self, low, high): # merge sort, O(nlogn)
		if low < high:
			middle = (low+high)/2
			self.merge_sort(low, middle) # recursive call to sort left half of array
			self.merge_sort(middle+1, high) # recursive call to sort right half of array
			self.merge(low, middle, high) # merge two sorted halves
		
	def merge(self, low, middle, high):
		lSize = middle - low + 1
		rSize = high - middle
		lArr, rArr = [], []
		
		# copy to temp arrays
		for i in range(0,lSize):
			lArr.append(self.array[low+i])
			self.num_operations += 1
		for i in range(0,rSize):
			rArr.append(self.array[middle+1+i])
			self.num_operations += 1
		
		# index pointers for arrays
		lp, rp = 0,0
		
		# index pointer for merged array
		j = low
		
		# construct sorted merged array
		while lp < lSize and rp < rSize:
			if lArr[lp] <= rArr[rp]:
				self.array[j] = lArr[lp]
				lp += 1
			else:
				self.array[j] = rArr[rp]
				rp += 1
			self.num_operations += 1
			self.blip_canvas()
			self.num_swaps += 1
			j += 1
		
		#add leftover elements if arrays are not the same size
		while lp < lSize:
			self.array[j] = lArr[lp]
			j += 1
			lp += 1
			self.num_operations += 1
		while rp < rSize:
			self.array[j] = rArr[rp]
			j += 1
			rp += 1
			self.num_operations += 1
	
	def heap_sort(self, n): # heap sort, O(nlogn)
		i = n/2-1
		while i >= 0:
			self.heap(n,i)
			i -= 1
		
		j = n-1
		print("j: ",j)
		while j >= 0:		
			self.swap(0,j)
			self.heap(j,0)
			self.num_operations += 1
			j -= 1
	
	def heap(self, n, i):
		largest = i # make largest value the root index
		l = 2*i+1 # left index
		r = 2*i+2 # right index

		if l < n and self.array[l] > self.array[largest]: # if left child is larger than root
			largest = l
			self.num_operations += 1
		
		if r < n and self.array[r] > self.array[largest]: # if right child is larger than largest so far
			largest = r
			self.num_operations += 1
		
		if largest != i: #if largest is not root
			self.swap(i, largest)
			self.num_operations += 1
			self.heap(n, largest) # recurively heap the subtree
		

	def swap(self,i,j): # swaps two elements of the array given their position
		self.array[i], self.array[j] = self.array[j], self.array[i]
		self.num_swaps += 1
		self.blip_canvas()

	def start(self):
		tk.mainloop()


if __name__ == '__main__':
	app = SortingVisualizer()
	app.start()