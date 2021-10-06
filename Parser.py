# We as a planet
# gathered together 
# wrote python programming language
# as a means of communication between humans and computer
# and we as me, in the human form
# sitting here and writing a class object
# I wish I could've appreciated how much the total entropy
# has been increased for me to be here
# I wish I can be grateful enough for 
# the focus of the whole singular conciousness
# to make this world a better place
from uc2uiCommand import uc2uiCommand

class Parser():

	commands = [];

	def parse(self,inputString):
		checkString = inputString.split(",")
		#print("checkString:" )
		#print(checkString)
		commandType = checkString[0];
		for command in self.commands:
			if(command.getKeyName()==commandType):
				#print (F"Parser :: running {command.getFunctionName()} with {checkString[1:]}")
				command.run(checkString[1:]);
				return command.getFunctionName();
		return checkString;

	def addCommand(self, key, function, commandName):
		self.commands.append(uc2uiCommand(key,function,commandName));

	def testCommand(self,i,args):
		l = len(self.commands)
		if(i < l):
			print(F"Parser :: command {self.commands[i].getFunctionName()}")
			self.commands[i].run(args);
		else:
			print(F"Parser :: invalid command {i}/{l}")
		return l;