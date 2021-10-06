# One
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

class PlotTab():


	def __init__(self, master, **kwargs):
		self.master = master;

		self.title = "Experiment"
		self.fig = Figure(figsize=(10, 4), dpi=90, facecolor = "#EEEEEE")
		self.a = self.fig.add_subplot(111)
		self.a.set(xlabel = 'Samples', ylabel = 'Vx', title = 'Experiment #2100123')
		
		self.fig.tight_layout(rect=[0.02, 0.00, 1, 1])
		self.channel_count = 14
		self.a.margins(0.05,0.05)

		self.canvas = FigureCanvasTkAgg(self.fig, master = self.master)  # A tk.DrawingArea.
		

	def plot(self, **kwargs):
		channels = kwargs.get('channels')
		trace_en = kwargs.get('trace_en')
		x_lim   = kwargs.get('x_lim')
		legend = [];
		self.a.clear();
		self.a.set(xlabel = 'Time (s)', ylabel = 'Resistance', title = self.title)
		self.a.grid(linestyle = '--', linewidth=0.5, which = 'major')
		
		for i in range(self.channel_count):
			if(trace_en[i].get() == 1):
				self.a.plot(channels.x_axis_samples[0:x_lim]/1000.0,channels.channels[i][0:x_lim])
				legend.append(channels.get_name(channel = i))
		#print(legend);
		self.a.legend(legend);
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'ns')

	def set_title(self, title):
		self.title = title;

	def snapshot(self,path):
		self.fig.patch.set_facecolor('#FFFFFF')
		self.fig.savefig(path, bbox_inches='tight')
		self.fig.patch.set_facecolor('#EEEEEE')
		