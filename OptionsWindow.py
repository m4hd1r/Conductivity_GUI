import tkinter as tk
from tkinter import ttk
import random

class OptionsWindow():
	num_of_channels = 14;

	def __init__(self, master, return_function):
		self.master = master;
		self.return_function = return_function;
		self.trace_en = [];
		self.past_trace_en = [];
		for i in range(self.num_of_channels):
			self.trace_en.append(tk.IntVar())
			self.trace_en[i].set(0)
			# some place to store the values and retrive them if didn't want to save
			self.past_trace_en.append(tk.IntVar()) 
			self.past_trace_en[i].set(0)
		#self.trace_en[0].set(1)
		#self.trace_en[1].set(1)
		#self.trace_en[2].set(1)
		#self.trace_en[3].set(1)
		self.trace_en[3].set(1)
		self.trace_en[4].set(1)

		self.past_x_axis 	= tk.IntVar(); 
		self.x_axis 		= tk.IntVar(); # select between time or samples?!
		self.x_lim_min      = 0;
		self.x_lim_max      = 300;
		self.preset = tk.StringVar()
	
	def set_x_lim_max(self, x_lim_max):	
		self.x_lim_max = x_lim_max;

	def get_trace_en(self):
		return self.trace_en;
	
	def get_xlim_max(self):
		return self.x_lim_max;

	def auto_x_set(self):
		return;
	def show(self):
		self.window = tk.Toplevel(self.master)
		self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
		plot_options_frame = ttk.LabelFrame(self.window, text = "");
		plot_options_frame.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = 'we')

		
		x_axis_frame = ttk.LabelFrame(self.window, text = "X Axis Settings")
		x_axis_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')
		self.past_x_axis.set(self.x_axis.get())
		x_axis_option_s = ttk.Radiobutton (x_axis_frame
			, text 		= "Samples"
			, variable 	= self.x_axis
			, value 	= 0)
		x_axis_option_t = ttk.Radiobutton (x_axis_frame
			, text 		= "Time"
			, variable 	= self.x_axis
			, value 	= 1)
		#x_axis_label 	= ttk.Label(x_axis_frame, text = "x axis unit")
		
		#x_axis_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
		x_axis_option_s.grid(row = 1, column = 0, padx = 2, pady = 2, sticky = 'we')
		x_axis_option_t.grid(row = 2, column = 0, padx = 2, pady = 2, sticky = 'we')

		x_axis_lim_min_label = ttk.Label(x_axis_frame, text = "min ")
		x_axis_lim_max_label = ttk.Label(x_axis_frame, text = "max ")
		
		
		self.x_axis_lim_min_entry = ttk.Entry(x_axis_frame, width = 10, justify = 'center')
		self.x_axis_lim_min_entry.insert(0,str(self.x_lim_min));
		self.x_axis_lim_max_entry = ttk.Entry(x_axis_frame, width = 10, justify = 'center')
		self.x_axis_lim_max_entry.insert(0,str(self.x_lim_max))

		x_axis_lim_min_label.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = 'we')
		x_axis_lim_max_label.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = 'we')
		self.x_axis_lim_min_entry.grid(row = 1, column = 2, padx = 2	, pady = 2, sticky = 'we')
		self.x_axis_lim_max_entry.grid(row = 2, column = 2, padx = 2, pady = 2, sticky = 'we')

		x_axis_auto_button = ttk.Button(x_axis_frame, width = 8, text = "Auto", command = self.auto_x_set)
		x_axis_auto_button.grid(row = 1, column = 3, padx = 2, pady = 2, rowspan = 2)

		trace_enable_frame = ttk.LabelFrame(self.window, text = "Traces Enable")
		
		trace_enable_frame.grid(row = 2, column = 0, padx = 5, pady = 2)
		trace_CB = [];
		trace_en_padx = 5;
		trace_en_pady = 5;
		trace_en_sticky = 'we'
		
		for i in range(self.num_of_channels):
			self.past_trace_en[i].set(self.trace_en[i].get())
			trace_CB.append(ttk.Checkbutton(trace_enable_frame
				, text		=	"CH  " + str(i+1)
				, variable 	= self.trace_en[i], onvalue=1, offvalue=0))
			
			trace_CB[i].grid(row = int(i/4), column = i%4, 
				padx 		= trace_en_padx, 
				pady 		= trace_en_pady, 
				sticky 		= trace_en_sticky)

		presets = ['user','preset 1', 'preset 2', 'preset 3']
		
		preset_traces_combo = ttk.Combobox(trace_enable_frame, width = 10, justify = 'center', textvariable = self.preset)
		self.preset.set('user')
		preset_traces_combo['values'] = presets
		preset_traces_combo['state'] = 'readonly'
		preset_traces_combo.bind('<<ComboboxSelected>>', self.preset_selected)
		preset_traces_combo.grid(row = 5, column = 0, padx = 2, pady = 2)
		all_traces_on_button = ttk.Button(trace_enable_frame, text = "All ON", width = 14, command = self.all_traces_on)
		all_traces_on_button.grid(row = 5, column = 1, padx = 2, pady = 2)
		all_traces_off_button= ttk.Button(trace_enable_frame, text = "All OFF", width = 14, command = self.all_traces_off)
		all_traces_off_button.grid(row = 5, column = 2, padx = 2, pady = 2)
		i_feel_lucky_button = ttk.Button(trace_enable_frame, text = "Im feeling lucky", width = 14, command = self.I_feel_lucky)
		i_feel_lucky_button.grid(row = 5, column = 3, padx = 2, pady = 2)

		
		save_button = ttk.Button(self.window, text = "Apply", command = self.save)
		save_button.grid(row = 10, column = 0, padx = 5, pady = 5 )
		
	def preset_selected(self,*args):
		preset1 = [1,1,1,1,1,1,1,1,0,0,0,0,0,0]
		preset2 = [0,0,0,0,0,0,0,0,1,1,1,1,0,0]
		preset3 = [0,0,0,0,0,0,0,0,0,0,0,0,1,1]
		print(self.preset.get())
		if(self.preset.get() == 'user'):
			return;
		for i in range(self.num_of_channels):
			if(self.preset.get() == 'preset 1'):
				self.trace_en[i].set(preset1[i])	
			elif(self.preset.get() == 'preset 2'):
				self.trace_en[i].set(preset2[i])
			elif(self.preset.get() == 'preset 3'):
				self.trace_en[i].set(preset3[i])

	def save(self):
		self.x_lim_max = int(self.x_axis_lim_max_entry.get())
		self.x_lim_min = int(self.x_axis_lim_min_entry.get())
		self.return_function(1)
		self.window.destroy();
		pass;

	def all_traces_on(self):
		for i in range(self.num_of_channels):

			self.trace_en[i].set(1)
	def all_traces_off(self):
		for i in range(self.num_of_channels):
			self.trace_en[i].set(0)
	def I_feel_lucky(self):
		for i in range(self.num_of_channels):
			self.trace_en[i].set(random.randrange(2))

	def on_closing(self):
		for i in range(self.num_of_channels): # return back to whatever it was before
			self.trace_en[i].set(self.past_trace_en[i].get())
		self.x_axis.set (self.past_x_axis.get())


		self.return_function(0)
		self.window.destroy();
		pass;
