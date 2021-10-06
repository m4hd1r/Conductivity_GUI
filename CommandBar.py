#one
import tkinter as tk
from tkinter import ttk
from CommandButton import CommandButton
class CommandBar():

	def __init__(self, parent, **kwargs):
		
		self.new_file 			= kwargs.get('new_file','')
		self.load_file 			= kwargs.get('load_file','')
		self.save_file 			= kwargs.get('save_file','')
		self.run_experiment 	= kwargs.get('run_experiment','')
		self.pause_experiment 	= kwargs.get('pause_experiment','')
		self.stop_experiment 	= kwargs.get('stop_experiment','')
		self.serial_connect 	= kwargs.get('serial_connect','')
		self.serial_disconnect 	= kwargs.get('serial_disconnect','')
		self.config_plot		= kwargs.get('config_plot','')
		self.capture_plot 		= kwargs.get('capture_plot','')
		self.exit 				= kwargs.get('exit','')
		
		
		self.command_frame = ttk.Frame(parent)
		
		
		self.new_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.new_file
			, idle_image = 		'graphics/document.png')
		
		self.new_button.grid(row = 0, column = 0);

		self.load_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.load_file
			, idle_image = 		'graphics/folder.png')
		
		self.load_button.grid(row = 0, column = 1);

		self.save_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.save_file
			, idle_image = 		'graphics/floppy-disk.png')
		
		self.save_button.grid(row = 0, column = 2);
		
		self.run_button = CommandButton(self.command_frame
			, behavior = 		'flippable'
			, command = 		self.run_experiment
			, second_command = 	self.pause_experiment
			, idle_image = 		'graphics/flask_idle.png'
			, second_image = 	'graphics/flask_running.png')
		
		self.run_button.grid(row = 0, column = 3);
		self.run_button.disable();

		self.stop_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.stop_experiment
			, idle_image = 		'graphics/stop.png')
		
		self.stop_button.grid(row = 0, column = 4);
		self.stop_button.disable();

		self.connect_button = CommandButton(self.command_frame
			, behavior = 		'flippable'
			, command = 		self.serial_connect
			, second_command = 	self.serial_disconnect 
			, idle_image = 		'graphics/cable-connector.png'
			, second_image = 	'graphics/cable-connected.png')
		
		self.connect_button.grid(row = 0, column = 5);

		self.config_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.config_plot
			, idle_image = 		'graphics/settings.png')

		self.config_button.grid(row = 0, column = 6);

		self.capture_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.capture_plot
			, idle_image = 		'graphics/camera.png')
		
		self.capture_button.grid(row = 0, column = 7);

		self.exit_button = CommandButton(self.command_frame
			, behavior = 		'function'
			, command = 		self.exit
			, idle_image = 		'graphics/power.png')
		
		self.exit_button.grid(row = 0, column = 8);

	def grid(self,**kwargs):
		row = kwargs.get('row',0);
		col = kwargs.get('column',0)
		rsp = kwargs.get('rowspan',1)
		self.command_frame.grid(row = row,column = col, rowspan = rsp)