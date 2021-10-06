#One
import tkinter as tk
from tkinter import ttk
from LabelEntry import LabelEntry
import csv
import numpy as np

class SettingTab():

	def __init__(self,master,**kwargs):
		
		self.col_frames = []
		self.col1_name = 'Experiment Info'
		self.col1 = [];
		self.data_callback = kwargs.get('data_callback');

		self.col1_fields = 	[
							['Date (Created)',			'' 			, 1, 0],
							['Julian Date',				''			, 0, 0],
							['Experiment ID',			''			, 0, 0],
							['Series ID',				''			, 1, 0],
							['Run No.',					''			, 1, 0],
							['Hardware Version',		''			, 0, 1],
							['uC Software Version',		''			, 0, 1],
							['Logging Period [s]',		''			, 0, 0],
							['Sampling Rate [ms]',		''			, 0, 0],
							['Acq. Start Date',			''			, 0, 1],
							['Acq. Start Time',			''			, 0, 1]]
		
		
		self.col2_name = 'Statistics'
		self.col2 = [];
		self.col2_fields = 	[
							['Windows Width [smp]',		''			, 0, 0],
							['Noise Level CH1  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH2  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH3  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH4  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH5  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH6  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH7  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH8  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH9  [uV]',	'0.0'		, 0, 1],
							['Noise Level CH10 [uV]',	'0.0'		, 0, 1],
							['Noise Level CH11 [uV]',	'0.0'		, 0, 1],
							['Noise Level CH12 [uV]',	'0.0'		, 0, 1],
							['Noise Level CH13 [uV]',	'0.0'		, 0, 1],
							['Noise Level CH14 [uV]',	'0.0'		, 0, 1]]
													
		
		
		self.col3_name = 'Sensor Types'
		self.col3 = [];
		self.col3_fields = 	[
							['External Ref Type',		''			, 0, 0],
							['CH1  Sensor  Type',		''			, 0, 0],
							['CH2  Sensor  Type',		''			, 0, 0],
							['CH3  Sensor  Type',		''			, 0, 0],
							['CH4  Sensor  Type',		''			, 0, 0],
							['CH5  Sensor  Type',		''			, 0, 0],
							['CH6  Sensor  Type',		''			, 0, 0],
							['CH7  Sensor  Type',		''			, 0, 0],
							['CH8  Sensor  Type',		''			, 0, 0],
							['CH9  Sensor  Type',		''			, 0, 0],
							['CH10 Sensor  Type',		''			, 0, 0],
							['CH11 Sensor  Type',		''			, 0, 0],
							['CH12 Sensor  Type',		''			, 0, 0],
							['CH13 Sensor  Type',		''			, 0, 0],
							['CH14 Sensor  Type',		''			, 0, 0]							
							];
		
		self.col_frame_n = 	[self.col1_name,	self.col2_name,		self.col3_name]
		self.cols = 		[self.col1,			self.col2,			self.col3]
		self.col_fields = 	[self.col1_fields, 	self.col2_fields, 	self.col3_fields]

		self.frame = ttk.Frame(master)
		

		

		## Constructing three columns 
		for j in range(3):
			self.col_frames.append(ttk.LabelFrame(self.frame, text = self.col_frame_n[j]))
			self.col_frames[j].grid(row = 0,column = j, padx = 5, pady = 5, sticky = 'nsew')
			i = 0
			for e in self.col_fields[j]:
				self.cols[j].append(LabelEntry(self.col_frames[j], label = e[0], text = e[1],spin = e[2], readonly = e[3],width = 20))
				self.cols[j][i].grid(row = i, column = 0,pady = 2, sticky = 'nsew')
				i = i + 1;
		self.frame.columnconfigure(0, weight = 1)
		self.frame.columnconfigure(1, weight = 1)
		self.frame.columnconfigure(2, weight = 1)


	def grid(self,**kwargs):
		row = kwargs.get('row',0)
		col = kwargs.get('column',0)
		col_span = kwargs.get('columnspan',1)

		self.frame.grid(row = row, column = col, columnspan = col_span, sticky = 'nsew')

	def get(self, **kwargs):
		field_name = kwargs.get('field','')
		for j in range(3):
			i = 0
			for e in self.col_fields[j]:
				if(e[0] == field_name):
					return self.cols[j][i].get()
				i = i + 1
		
	def set(self, **kwargs):
		field_name 	= kwargs.get('field','')
		value		= kwargs.get('value','')
		#print(F"setting {field_name} to {value}")
		for j in range(3):
			i = 0
			for e in self.col_fields[j]:
				if(e[0] == field_name):
					self.cols[j][i].set(value)
					#print(F"{field_name} set to {self.cols[j][i].get()}")
					return
				i = i + 1
	
	def save(self,**kwargs):
		file_name = kwargs.get('file_name','default.csv')
		chns = kwargs.get('channels')
		data_len = kwargs.get('clen')
	
		#print(F"saving")
			
		for j in range (3):
			i = 0
			for e in self.col_fields[j]:
				e = [e[0], (self.get(field = e[0])), 0 , 0]
				self.col_fields[j][i] = e;
				#print(F"j = {j} i = {i} :: {e}")
				i = i + 1;
		#print(self.col_fields[0])
		with open (file_name,'w+',newline='') as csv_file:
			new_array = csv.writer(csv_file)
			new_array.writerow(['col1'])
			new_array.writerows(self.col_fields[0])
			new_array.writerow(['col2'])
			new_array.writerows(self.col_fields[1])
			new_array.writerow(['col3'])
			new_array.writerows(self.col_fields[2])
			new_array.writerow(['endsetting'])
			
			for i in range(data_len):
				row = []
				row.append(i)
				row.append(chns.x_axis_samples[i])
				for j in range(14):
					row.append (chns.get_point(channel = j, index = i));

				new_array.writerow(row)
			new_array.writerow(['enddata'])
			
	
	def fill_table(self):
		for j in range(3):
			i = 0
			#print (F"J = {j}")
			for e in self.col_fields[j]:
				#print(e)
				text = e.split(',')[1]
				text = text[2:len(text)-1]
				self.cols[j][i].set(text)
				i = i + 1

	def load(self, **kwargs):
		file_name = kwargs.get('file_name','default.csv')
		with open (file_name) as csv_file:
			rows = list(csv.reader(csv_file, delimiter = ','))
			j = 0;
			i = 0;
			for row in rows:
				i = i + 1;
				if(row[0] == 'col1'):
					j = 0
				elif(row[0] == 'col2'):
					j = 1
				elif(row[0] == 'col3'):
					j = 2
				elif(row[0] == 'endsetting'):
					i = 0;
					j = 3
				elif(row[0] == 'enddata'):
					j = 4
					break
				if (len(row)>1 and j < 3):
					self.set(field = row[0], value = row[1])
				#print(row[0].isnumeric())
				if(j == 3):
					#print(F"{i} {row}")
					try:
						float(row[0])
						self.data_callback(row)
					except ValueError:
						pass;
				#print(F'rowset {j} -row[0]: {row[0]}-{len(row)}- {row}')
				#print(F'{j} + {row} +len: {len(row)}')
		#print(F"fields[0] = {fields[0]}")
		#print(F"fields[2] = {fields[2]}")
		#print(F"fields[4] = {fields[4]}")
		#print(*self.col_fields[0],sep = "\n ")
		#self.fill_table();