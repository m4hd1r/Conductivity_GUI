# It's been 7 whole days

import numpy as np

class Channels():


	def __init__(self, **kwargs):
		self.channels = []
		self.channel_names = []
		self.trace_enable = []
		self.trace_name_has_been_changed = []
		self.num_of_channels = 0
		self.channel_length = 50000
		self.x_axis_samples = np.zeros(self.channel_length);

	def assert_indicies(self, **kwargs):

		index = kwargs.get('index',-1)
		channel = kwargs.get('channel',-1)

		if(index > 0):
			if(index >= self.channel_length):
				print (F'Channels :: ERR: index {index} out of bound')
				return 0;
		
		if(channel > 0):
			if(channel < 0 or channel > self.num_of_channels):
				print ('Channels :: ERR: channel out of bound')
				return 0;
		
		return 1;

	def get_point(self, **kwargs):

		channel = kwargs.get('channel',0)
		index = kwargs.get('index', 0)

		if(self.assert_indicies(channel = channel, index = index)==0):
			
			return -1
		#print(F'channel {channel} , index {index}')
		return self.channels[channel][index];

	def set_point(self, **kwargs):

		channel = kwargs.get('channel',0)
		index = kwargs.get('index', 0)
		value = kwargs.get('value',0)

		if(self.assert_indicies(index = index, channel = channel)==0):
			return -1

		self.channels[channel][index] = value

	def get_channel(self, **kwargs):

		channel = kwargs.get('channel',0)
		if(self.assert_indicies(channel = channel)==0):
			return -1
	
		return channels[channel]

	def add_channel(self, **kwargs):

		channel_name = kwargs.get('name')
		

		self.channels.append(np.zeros(self.channel_length))
		self.channel_names.append(channel_name)
		self.trace_name_has_been_changed.append(1)
		self.trace_enable.append(1)
		#self.channels[self.num_of_channels][0] = self.num_of_channels;
		self.num_of_channels += 1

	def set_name(self, **kwargs):

		channel = kwargs.get('channel', 0)
		new_name = kwargs.get('name', '')

		if(self.assert_indicies(channel = channel)==0):
			return -1
		
		self.channel_names[channel] = new_name;
		self.trace_name_has_been_changed[channel] = 1;
		
	def get_name(self, **kwargs):

		channel = kwargs.get('channel',0)

		if(self.assert_indicies(channel = channel)==0):
			return -1
		
		self.trace_name_has_been_changed[channel] = 0;
		return self.channel_names[channel]

	def name_changed(self, **kwargs):

		channel = kwargs.get('channel',0)

		if(self.assert_indicies(channel = channel)==0):
			return -1

		return self.trace_name_has_been_changed[channel]

	def visible(self,**kwargs):

		channel = kwargs.get('channel',0)
		
		if(self.assert_indicies(channel = channel)==0):
			return -1
		
		return self.trace_enable[channel]

	def set_enable_to(self,**kwargs):

		channel = kwargs.get('channel',0)
		en = kwargs.get('enable', 1)

		if(self.assert_indicies(channel = channel)==0):
			return -1
		
		self.trace_enable[channel] = en
	
	
	def save(self,**kwargs):

		file_name = kwargs.get('file_name','default.csv');

		np.savetxt(file_name,self.channels,delimiter=',')
		print('saved');
	
	def load(self,**kwargs):

		file_name = kwargs.get('file_name', 'default.csv')
		
		self.channels = np.read_csv(file_name,delimiter=',')
		print(self.channels)

	def load_channel(self, **kwargs):
		channel_index = int(float(kwargs.get('index')))
		channel_data  = np.array(kwargs.get('channel_data'))
		channel_data_float = channel_data.astype(np.float)
		
		#print(F"loading {channel_index} ::{channel_data_float}")
		if(self.assert_indicies(channel = channel_index)==0):
			#print(F'Huston {channel_index} is not my thing')
			return -1;

		#self.channels[(channel_index)] = [channel_index,(channel_data_float), np.zeros(len(self.channel_length-channel_data_float-1))];
		self.channels[channel_index] = np.zeros(1)+channel_index;
		self.channels[channel_index] = np.append(self.channels[channel_index], channel_data_float);
		self.channels[channel_index] = np.append(self.channels[channel_index],np.zeros((self.channel_length)-len(channel_data_float)-1))
		#self.channels[channel_index].append(channel_data_float);
		#self.channels[channel_index].append(np.zeros(len(self.channel_length-channel_data_float-1)));

		#print(F'channels{channel_index} len({len(self.channels[channel_index])}) = {self.channels[channel_index]}')
		return; 
