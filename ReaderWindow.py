# One
import tkinter as tk
from tkinter import ttk
from SerialIO import SerialIO
from Parser import Parser
from LabelEntry import LabelEntry
from CommandButton import CommandButton
from CommandBar import CommandBar
from SettingTab import SettingTab
import julian
from Channels import Channels
from OptionsWindow import OptionsWindow
import numpy as np
from PlotTab import PlotTab
from DataTab import DataTab
from tkinter import filedialog
from tkinter import messagebox

import datetime

class ReaderWindow():
	a = 2;
	b = 3;
	
	def julian_date_task():

		return;

	def __init__(self, master):
		self.frame = (master);
		#self.frame.pack();
		self.fixed_title = 'Questat Flowcell Interface :: 2021'
		style = ttk.Style()
		master.title(self.fixed_title)
		#style.theme_use('vista')
		style.configure('TButton'	, width = 20, borderwidth=1, focusthickness=30, focuscolor='blue')
		style.map('TButton', background=[('active','green')])

		self.serial_frame_init()
		self.command_frame_init()
		self.notebook_init()
		self.status_bar_init()
		self.options_window = OptionsWindow(self.frame,self.config_returned);		
		self.trace_enable = self.options_window.get_trace_en();
		self.x_axis_samples = self.options_window.get_xlim_max();
		self.chn = Channels();
		
	
		self.main();


	def transfer_data_from_settings_to_channels(self,row):
		index = int(row[0])
		self.chn.x_axis_samples[index] = float(row[1])
		for i in range(14):
			self.chn.set_point(channel = i, index = index, value = float(row[i+2]))
		self.x_axis_samples = index+1;
		#print(F"passing {row[0]} size:{len(row[1:])}")
		#self.chn.load_channel(index = row[0], channel_data = row[1:])

	def func1(self, *args):
		print(F"Func1 {args[0][0]} \n");
	
	def func2(self, *args):
		print("Func2\n");

	def concat(self):
		self.button1.disable();
		return self.LabelEntry1.get() + "SS WW\n" 
	
	def command(self):
		print("1st command")
		self.button.enable();

	def second_command(self):
		print("2nd command")
		self.button.disable();

	def new_file(self):
		today = datetime.datetime.now()
		self.settingTab.set(field="Date (Created)",value=today.strftime("%b-%d-%Y"))
		#print()
		self.settingTab.set(field="Julian Date", value= int(np.floor(julian.to_jd(datetime.datetime.now(), fmt='jd')- 2440000.5)+1786))
		self.change_status_to('New file')
		return;

	def load_file(self):
		#print("load file called")
		directory = filedialog.askopenfilename(
			title="Load data"
			,filetypes=[("csv file", "*.csv")])
		if(directory != ""):
			self.settingTab.load(file_name = directory);
			self.load_data_to_table();
		self.change_status_to(F'{directory} has been loaded')
		#for j in range (5):
		#	for i in range (300):
		#		self.chn.set_point(channel = j, index = i, value = ((np.sin(i/300.0*2*np.pi*(j+2)))));
		#self.log_out_channels(300);
		return;

	def save_file(self):
		#print("save file called")
		directory = filedialog.asksaveasfilename(defaultextension='.csv'
			,title="Save data"
			,filetypes=[("csv file", "*.csv")])
		if(directory != ""):
			self.settingTab.save(file_name = directory,channels = self.chn, clen = self.x_axis_samples);
		self.change_status_to(F'Data has been saved into {directory}')
		return;

	def generate_title(self):
		JD = self.settingTab.get(field = "Julian Date");
		EXID = self.settingTab.get(field = 'Experiment ID');
		SD = self.settingTab.get(field = 'Series ID');
		RN = self.settingTab.get(field = 'Run No.');
		return str(JD)+'_'+str(EXID)+'_'+str(SD)+'_'+str(RN);

	def run_experiment(self):
		#self.serialIO.send("*,\n")
		#self.serialIO.send("S,50,1000\n")
		#print("run experiment called")
		self.serialIO.flush();
		setting_field = self.settingTab.get(field ='Logging Period [s]')
		if(setting_field == ""):
			return;
		logging_period = int(setting_field);
		setting_field = self.settingTab.get(field ='Sampling Rate [ms]')
		if(setting_field == ""):
			return;
		sampling_rate  = int(setting_field);
		if(sampling_rate < 45):
			tk.messagebox.showinfo('invalid sampling rate','Sampling rate cannot be less than 45ms')
			sampling_rate = 45;
			self.settingTab.set(field = 'Sampling Rate [ms]',value = sampling_rate);
			 
		if(logging_period/sampling_rate*1000 > 50000):
			tk.messagebox.showinfo('Tons of data points','Number of sampled points is limited to 50k')
			logging_period = (int)(50*sampling_rate);
			self.settingTab.set(field = 'Logging Period [s]',value = logging_period);
		#print(F"sampling rate: {sampling_rate} logging_period: {logging_period}");
		for i in range (14):
			j = i +1;
			if(j < 10):
				chn_name = self.settingTab.get(field = F"CH{j}  Sensor  Type")
			else:
				chn_name = self.settingTab.get(field = F"CH{j} Sensor  Type")
			print(chn_name )
			self.chn.set_name(channel = i, name = chn_name)
		
		setting_field = self.settingTab.get(field ='0: 12.5kHz 1:6.25kHz')
		frequency_selection = int(setting_field);
		if(frequency_selection != 0 and frequency_selection != 1):
			frequency_selection = 0
			self.settingTab.set(field = '0: 12.5kHz 1:6.25kHz', value = 0)
		command = "freq,"+ str(frequency_selection)+"\n"
		self.serialIO.send(command)
		command = "run," + str(logging_period) + "," + str(sampling_rate) + "\n"
		self.serialIO.send(command); 
		self.change_status_to(F'Running the experiment with sampling rate of {sampling_rate}ms and total length of {logging_period}s | {logging_period/60:.2f}mins | {logging_period/3600:.2f}hours | {(2-frequency_selection)*6.25:.2f}kHz')
		return 1;

	def pause_experiment(self):
		self.serialIO.send("pause\n")
		self.serialIO.flush()
		print("pause experiment called")
		self.change_status_to('The experiment has been paused')
		return 1

	def stop_experiment(self):
		self.serialIO.send("stop\n")
		self.serialIO.flush();
		self.commandbar.run_button.go_idle()
		print("stop experiment called")
		self.change_status_to('The experiment has been stopped')
		return 1;

	def serial_connect(self):
		print("serial connect called")
		self.serialIO.flush();
		if(self.serialIO.connect() == 1):
			self.commandbar.run_button.enable();
			self.commandbar.stop_button.enable();
			self.serialIO.send("introduce\n")
			self.change_status_to('Serial connection through COM port was successful')
			return 1;
		else:
			self.change_status_to('Something went wrong with the serial connection, check logs')
			return 0;


	def serial_disconnect(self):
		self.commandbar.stop_button.disable();
		self.commandbar.run_button.disable();
		self.change_status_to('COM port is closed')
		return self.serialIO.disconnect()
	
	def capture_plot(self):
		print("capture plot called")
		directory = filedialog.asksaveasfilename(defaultextension='.png'
			,title="Save data"
			,filetypes=[ ("png file", "*.png")
						,("tiff file", "*.tiff")])
		if(directory != ""):
			self.plotTab.snapshot(directory);
			self.change_status_to(F"The snapshot has been saved in {directory}")
			return;
		self.change_status_to("I think you have changed your mind about saving that file")	
		return;
	
	def config_plot(self):
		self.options_window.set_x_lim_max(self.x_axis_samples);
		self.options_window.show();
		self.commandbar.config_button.disable()
		print("config plot called")
		return;

	def config_returned(self,save):
		print(F"config returned with {save}")
		self.trace_enable = self.options_window.get_trace_en();
		self.x_axis_samples = self.options_window.get_xlim_max();
		self.commandbar.config_button.enable()
		self.load_data_to_table();

	def exit(self):
		#self.log_out_channels(self.x_axis_samples);
		print("exit called")
		self.frame.destroy();
		return;

	def status_bar_init(self):
		self.status_text = tk.StringVar();
		self.status_text.set("Hello")
		self.statusBar = ttk.Label(self.frame,textvariable = self.status_text);
		self.statusBar.grid(row = 2,column = 0, padx = 5, pady = 2, sticky = 'we')
	
	def change_status_to(self,text):
		self.status_text.set(text);		
	def command_frame_init(self):
		
		self.commandbar_frame = ttk.LabelFrame(self.frame);

		self.commandbar = CommandBar (self.commandbar_frame
			,new_file 			= self.new_file 			
			,load_file 			= self.load_file 			
			,save_file 			= self.save_file 			
			,run_experiment 	= self.run_experiment 	
			,pause_experiment 	= self.pause_experiment 
			,stop_experiment 	= self.stop_experiment 
			,serial_connect 	= self.serial_connect 	
			,serial_disconnect	= self.serial_disconnect
			,config_plot		= self.config_plot
			,capture_plot 		= self.capture_plot 		
			,exit 				= self.exit 					
			)
		self.commandbar_frame.grid(row = 0, column = 0, padx = 2, pady = 2)
		self.commandbar.grid(row = 0, column = 0, padx = 2, pady = 2)

	def process_data_frame(self, *args):
		index = int(args[0][0]);
		t = int(args[0][1]);
		self.chn.channel_length = index+2;
		self.chn.x_axis_samples[index] = t;
		self.x_axis_samples = index+1;
		d = [];
		data_len = len(args[0])-2;
		#print(F"index: {index}, t:{t}, {args[0]}")
		for i in range(data_len):
			d.append(float(args[0][i+2]))
			self.chn.set_point(channel = i, index = index,value = d[i]);
	
	def info_log(self, *args):
		#self.change_status_to('An info message from uC is received')
		print (args[0][0]);
		
	def pop_op_info(self, *args):
		#self.change_status_to('A pop-up info message from uC is received')
		tk.messagebox.showinfo('info',args[0][0]);


	def hw_sw_info(self, *args):
		self.settingTab.set(field = "Hardware Version",value = args[0][0])
		self.settingTab.set(field = "uC Software Version", value = args[0][1])

	def start_time_stamp(self, *args):
		now = datetime.datetime.now();
		self.settingTab.set(field = "Acq. Start Date", value = now.strftime("%b-%d-%Y"))
		self.settingTab.set(field = "Acq. Start Time", value = now.strftime("%H:%M:%S"))
		


	def serial_frame_init(self):
		self.serial_parser = Parser();
		self.serial_parser.addCommand("D",self.process_data_frame,"process_data_frame");
		self.serial_parser.addCommand("i",self.info_log,"info log")
		self.serial_parser.addCommand("w",self.pop_op_info,"pop up info")
		self.serial_parser.addCommand("v",self.hw_sw_info,"hw sw info")
		self.serial_parser.addCommand("t",self.start_time_stamp,"start time stamp")
		
		
		#self.serial_parser.addCommand("S",self.func2,"func2Name");
		#self.serial_parser.parse("key2,2,3");

		self.serial_frame = ttk.LabelFrame(self.frame);
		self.serial_frame.grid(row = 0, column = 1, pady = 2, padx = 2, sticky = 'nsew')
		self.serialIO = SerialIO(self.serial_frame, self.serial_parser)


	def notebook_init(self):
		self.tab_parent = ttk.Notebook(self.frame)

		self.setting_tab 	= ttk.Frame(self.tab_parent)
		self.plot_tab 	  	= ttk.Frame(self.tab_parent)
		self.data_tab		= ttk.Frame(self.tab_parent)

		self.tab_parent.add (self.setting_tab, text = "Settings")
		self.tab_parent.add (self.plot_tab, text = "Plots")
		self.tab_parent.add (self.data_tab, text = "Data")
		self.tab_parent.grid(row = 1, column = 0, padx = 2, pady = 2, columnspan = 2, sticky = 'nsew')
		self.tab_parent.bind("<<NotebookTabChanged>>", self.tab_changed_callback)	
	
	def load_data_to_table(self):
			#print("updating table")
			self.dataTab.update_table(channels = self.chn, x_lim = self.x_axis_samples);
	
	def tab_changed_callback(self,event):
		if (event.widget.tab(event.widget.select(), "text") == "Data"):
			self.load_data_to_table();
		elif(event.widget.tab(event.widget.select(), "text") == "Plots"):
			self.plotTab.set_title(self.generate_title());

	def log_out_channels(self,m_range):
		for i in range (m_range-1):
			print(	F"{i}:" +
					F"{self.chn.get_name(channel = 0)}: {self.chn.get_point(channel = 0, index = i)} \t" +
					F"{self.chn.get_name(channel = 1)}: {self.chn.get_point(channel = 1, index = i)} \t" +
					F"{self.chn.get_name(channel = 2)}: {self.chn.get_point(channel = 2, index = i)} \t" +
					F"{self.chn.get_name(channel = 3)}: {self.chn.get_point(channel = 3, index = i)} \t" +
					F"{self.chn.get_name(channel = 4)}: {self.chn.get_point(channel = 4, index = i)} ")
	
	def update_bit_rate(self):
		pass;

	def update_plot(self):
		self.plotTab.plot(channels = self.chn,trace_en = self.trace_enable, x_lim = self.x_axis_samples)
		#print(self.chn.channels[0])
		self.frame.after(100,self.update_plot)
		
	#def beep(self):
	#	fp = 2000;
	#	fs = 44100;
	#	t = np.arange(0,.1,1/fs);
	#	data = 0.1*np.sin(fp*2*np.pi*t);
	#	sd.play(data, fs)
		
	#	self.frame.after(300, self.beep)

	def main(self):
		

		#self.SerialIO.connect(115200,'COM12')
		#data = np.random.uniform(-1, 1, fs)
		
		self.change_status_to("Graphics by various artists of Flaticon")
		
		self.chn.add_channel(name = "CHN0")
		self.chn.add_channel(name = "CHN1")
		self.chn.add_channel(name = "CHN2")
		self.chn.add_channel(name = "CHN3")
		self.chn.add_channel(name = "Conductivity1")
		self.chn.add_channel(name = "Conductivity2")
		self.chn.add_channel(name = "CHN6")
		self.chn.add_channel(name = "CHN7")
		self.chn.add_channel(name = "CHN8")
		self.chn.add_channel(name = "CHN9")
		self.chn.add_channel(name = "CHNA")
		self.chn.add_channel(name = "CHNB")
		self.chn.add_channel(name = "CHNC")
		self.chn.add_channel(name = "CHND")
		
		#self.log_out_channels(300);

		#self.chn.save();			

		
		self.settingTab = SettingTab(self.setting_tab,data_callback = self.transfer_data_from_settings_to_channels)
		self.settingTab.grid(row = 0, column = 0)
		self.plotTab = PlotTab(self.plot_tab)
		self.dataTab = DataTab(self.data_tab, channels = self.chn)
		self.update_plot()
		#	self.beep();

		#self.chn.get_channels();	
		#parser.runCommand(0,2,3);
		#parser.runCommand(1);
		#c1 = ui2ucCommand ("key",self.func1)
		#c1.run(self.a,self.b)
		#self.SerialIO.connect(115200,'COM15')
		#print(F"{self.SerialIO.get_ports()}");
		#print(self.SerialIO.get_bitrate())

