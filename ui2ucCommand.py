# All

class ui2ucCommand():

	def __init__(self,key,function, functionName):
		self.key = key;
		self.function = function;
		self.functionName = functionName

	def run(self,args):
		self.function(args)

	def getKeyName(self):
		return self.key

	def getFunctionName(self):
		return self.functionName;