# One
import tkinter as tk
from tkinter import ttk

class CommandButton():
	
	def sendCommand(self, **kwargs):
		if(self.behavior == 'static'):
			self.go_run()
			#print("Static Command Button " + self.text + " :: "+ self.command);
			self.io.send(self.command)
		elif(self.behavior == 'dynamic'):
			self.go_run()
			newCommand = self.command()
			#print("Dynamic Command Button " + self.text + " :: " + newCommand);
			self.io.send(newCommand)
		elif(self.behavior == 'function'):
			self.go_run()
			#print("Function Command Button " + self.text + " :: ");
			self.command()
		elif(self.behavior == 'flippable'):
			if(self.state == 'idle'):
				if (self.command() == 1) :
					self.state = 'second_command'
					self.button['image'] = self.second_image
			elif(self.state == 'second_command'):
				if(self.second_command()):
					self.state = 'idle'
					self.button['image'] = self.idle_image



	def __init__(self, parent, **kwargs):
		
		idle_image_address = kwargs.get('idle_image', '')
		hover_image_address = kwargs.get('hover_image', '')
		running_image_address = kwargs.get('running_image', '')
		second_image_address = kwargs.get('second_image','')
		width = kwargs.get('width',35)
		ss = 1
		self.noImage = 0;
		if(idle_image_address != ''):
			self.idle_image = tk.PhotoImage(file=idle_image_address)
			self.idle_image = self.idle_image.subsample(ss, ss)
		else:
			self.noImage = 1;
		
		if(second_image_address != ''):
			self.second_image = tk.PhotoImage(file=second_image_address)
			self.second_image = self.second_image.subsample(ss, ss)
		else:
			self.second_image = self.idle_image;
		

		if(hover_image_address != ''):
			self.hover_image = tk.PhotoImage(file=hover_image_address)
			self.hover_image = self.hover_image.subsample(ss, ss)
		elif(self.noImage == 0):
			self.hover_image = self.idle_image;

		if(running_image_address != ''):
			self.running_image = tk.PhotoImage(file=running_image_address)
			self.running_image = self.running_image.subsample(ss, ss)
		elif(self.noImage == 0):
			self.running_image = self.idle_image;

		self.state = 'idle'
		self.text = kwargs.get('text', 'command')
		self.command = kwargs.get('command', '')
		self.second_command = kwargs.get('second_command', '')
		self.io = kwargs.get('io','')
		self.parent = parent;
		self.behavior = kwargs.get('behavior', 'static')

		#self.style = ttk.Style();
		#self.style.configure('W.TButton',borderwidth = 52, background='#FFF')
		self.button = ttk.Button(parent,text = "Hey", command = self.sendCommand  ,width = width)
		if(self.noImage == 0):
			self.go_idle()
		self.button.bind("<Enter>", self.on_hover)
		self.button.bind("<Leave>", self.on_leave)
			
	
	def grid(self,**kwargs):
		row = kwargs.get('row', 0)
		col = kwargs.get('column', 0)
		self.button.grid(row = row, column = col, padx = 5, pady = 5);

	def on_hover(self, *args):
		if(self.state == 'idle'):
			self.button['image'] = self.hover_image;

	def on_leave(self, *args):
		if(self.state == 'run'):
			self.button['image'] = self.running_image;
		elif(self.state == 'idle'):
			self.button['image'] = self.idle_image;
	
	def go_run(self):
		self.state = 'run';
		self.button['image'] = self.running_image;
	
	def go_idle(self):
		self.state = 'idle'
		self.button['image'] = self.idle_image;

	def disable(self):
		self.state = 'disable'
		self.button['state'] = 'disabled'

	def enable(self):
		self.state = 'idle'
		self.button['state'] = 'normal'
	