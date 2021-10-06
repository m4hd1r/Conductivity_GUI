# coming back to life

import tkinter as tk
from tkinter import ttk

class DataTab():

	def __init__(self, master, **kwargs):
		
		self.channels = kwargs.get('channels')
		self.master = master
		self.channel_count  = 14

		self.content_frame = ttk.Frame(self.master,padding =(3,3,12,12))

		self.data_list = ttk.Treeview(self.content_frame);
		self.data_scroll = ttk.Scrollbar(self.content_frame,orient = 'vertical')
		self.x_scroll = ttk.Scrollbar(self.content_frame, orient = 'horizontal')

		self.data_scroll.configure(command=self.data_list.yview)
		self.x_scroll.configure(command=self.data_list.xview)
		
		self.data_list.configure(yscrollcommand=self.data_scroll.set, xscrollcommand=self.x_scroll.set)

		col_names = ['index','time'];
		for i in range(self.channel_count):
			col_names.append(self.channels.get_name(channel = i))
		
		self.data_list['columns'] = col_names;

		self.data_list.column("#0",width = 0, stretch = tk.NO);
		self.data_list.heading('#0', text = '', anchor = tk.CENTER)
		for col in col_names:
			self.data_list.column (col, anchor = tk.CENTER, width = 60, stretch = tk.NO) 
			self.data_list.heading(col, text = col,anchor = tk.CENTER)
		
		self.content_frame.columnconfigure(0, weight = 10)
		self.content_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nsew')
		self.data_scroll.grid(row = 0, column = 1, pady = 5, sticky = 'nsew')
		self.data_list.grid(row = 0, column = 0, pady = 5, sticky = 'nsew')
		self.x_scroll.grid(row = 1, column = 0, pady = 5, sticky = 'nsew')

	def update_table(self,**kwargs):
		channels 	= kwargs.get('channels')
		x_lim   	= kwargs.get('x_lim')

		self.data_list.delete(*self.data_list.get_children())
		for i in range (x_lim):
			row = [i];
			row.append(channels.x_axis_samples[i]);
			for j in range(self.channel_count):
				row.append(channels.get_point(channel = j, index = i))
			self.data_list.insert(parent = '',index=i, iid = i, values = row)
	
