# One


import tkinter as tk
from tkinter import ttk
import serial
import sys
import glob


class SerialIO():
	

	def bitrate_calc(self):
		self.bitrate =  0.5*self.bitrate + 0.5*self.serial_load * 8 * 2
		self.bitrate_label['text'] = "{:.0f}".format(self.bitrate) + "bps"
		self.serial_load = 0
		self.parent.after(500,self.bitrate_calc)


	def __init__(self, parent, parser):
		self.ser = serial.Serial(timeout=0)
		self.parser = parser
		self.parent = parent
		self.bitrate = 0
		self.serial_load = 0
		self.serBuffer = ""

		self.port_label = ttk.Label(self.parent,text = "Port")
		self.port_label.grid(row = 0 , column = 0)

		self.selected_port = tk.StringVar(self.parent)
		self.port_names = self.get_ports();
		self.selected_port.set("Port")
		#self.port_option_menu = OptionMenu(master, selected_port ,*port_names)
		self.port_combo_box = ttk.Combobox (self.parent, width = 13, justify = 'center' ,textvariable = self.selected_port)
		self.port_combo_box['values'] = self.port_names
		self.port_combo_box['state'] = 'readonly'
		self.port_combo_box.grid(row = 0, column = 1, padx = 5, pady = 3, sticky = 'ns')

		self.baudrate_label = ttk.Label(self.parent, text = "Baudrate")
		self.baudrate_label.grid(row = 1, column = 0, padx = 5, pady = 3, sticky = 'ns')
		
		self.baudrate_entry = ttk.Entry(self.parent, justify = 'center', width = 15)
		self.baudrate_entry.insert(0,"115200")
		self.baudrate_entry.grid(row = 1, column = 1, padx = 5, pady = 3, sticky = 'ns')

		self.bitrate_label = ttk.Label(self.parent, text = "bps")
		self.bitrate_label.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 3, sticky = 'ns')

		self.bitrate_calc()


	def get_ports(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		#elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
		#	ports = glob.glob('/dev/tty[A-Za-z]*')
		#elif sys.platform.startswith('darwin'):
		#	ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Serial :: Unsupported platform')
	
		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result

	def disconnect(self):
		if self.ser.is_open == True:
			self.ser.close()
			print("Serial :: Closed the serial port")
			return 1;

	def connect(self):
		self.ser.baudrate = self.baudrate_entry.get();
		self.flush();
		print(F"Serial :: Baudrate is set to {self.ser.baudrate}")
		if(self.ser.is_open == True):
			self.ser.close()
			print(F"Serial :: disconnected {self.ser.port}")
		if self.selected_port.get().startswith("COM") == True:
			self.ser.port = self.selected_port.get()
			print(F"Serial :: port is set to {self.ser.port}")
		else: 
			print("Serial :: Invalid serial port")
			return 0;
		self.ser.open()
		if self.ser.is_open == True:
			print ("Serial :: Connected Successfully")
			self.readSerial()
			return 1;

	def readSerial(self):
		while True:

			if self.ser.is_open == True:
				c = self.ser.read().decode()
			else: 
				break
			
			if len(c) == 0:
				break
			
			self.serial_load = self.serial_load + 1
	
			
			if c == '\r':
				c = '' 
				
			if c == '\n':
				self.parser.parse(self.serBuffer)
				self.serBuffer = "" 
			else:
				self.serBuffer += c 
		if self.ser.is_open == True:
			self.parent.after(100, self.readSerial) # check serial again soon
		else:
			return

	def send(self,command):
		self.writeSerial(command)

	def writeSerial(self, command):
		self.ser.write(command.encode())
		print(F"Serial :: command > {command}")
	
	def get_bitrate(self):
		return self.bitrate

	
	def flush(self):
		self.serBuffer = ""