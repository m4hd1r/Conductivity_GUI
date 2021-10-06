
import tkinter as tk
from tkinter import ttk
from CustomText import CustomText

class LabelEntry():

	def defaultCallback(self,event):
		print(self.text.get())
		return;

	def __init__(self,parent, **kwargs):

		self.frame = parent#ttk.Frame(parent)
		labelName = ""
		defaultText = ""

		defaultText = kwargs.get('text','')
		labelName = kwargs.get('label','label');
		return_callback = kwargs.get('callback',self.defaultCallback)
		spin = kwargs.get('spin',0)
		width = kwargs.get('width', 10)
		self.readonly = kwargs.get('readonly', 0)
		self.text = tk.StringVar();
		#labelName = kwargs.pop('label')
		#defaultText = kwargs.pop('text')
		#self.row_number = kwargs.pop('row')
		self.label = ttk.Label(self.frame,text = labelName)
		
		if(spin == 0):
			self.textBox = ttk.Entry(self.frame, textvariable = self.text, width = width ,justify = 'center')
		else:
			self.textBox = ttk.Spinbox(self.frame, textvariable = self.text, width = width, from_ = 0, to = 1000 ,justify = 'center')
		
		self.textBox.insert(0,defaultText)	
		if(self.readonly):
			self.textBox.config(state = "readonly")

		
		self.textBox.bind('<Return>', return_callback)

	def grid(self,**kwargs):
		#self.frame.grid(**kwargs);
		row = kwargs.get('row',0)
		col = kwargs.get('column',0)
		pady = kwargs.get('pady',5)
		self.textBox.grid(row = row, column = col+1, padx = 5, pady = pady, sticky = 'WE')
		self.label.grid(row = row, column = col, padx = 5, pady = pady, sticky = 'E')

	def get(self):
		return self.textBox.get();

	def set(self,text):
		if(self.readonly):
			self.textBox.config(state = 'normal')
		self.textBox.delete(0,'end')
		self.textBox.insert(0,text)
		if(self.readonly):
			self.textBox.config(state = "readonly")

	def new(self):
		self.set("");
