import discord
import copy
from discord.ext import commands
class gui:
#class vars and functions
	gui_arr = []
	def testUniq(Id):
		for g in gui.gui_arr:
			if g.Id == Id:
				return False
		return True
	def getUniqId():
		Id = 1
		while not gui.testUniq(Id):
			Id += 1
		return Id
	def getGuiId(Id):
		for g in gui.gui_arr:
			if g.Id == Id:
				return g
		return None

#object vars and functions
	def __init__(self,emojiList):
		self.Id = 0
		self.emojiL = emojiList
		#windows is a list of functions that take the gui obj and will return strings
		#they are used to order the gui and render it
		self.windows = []
	def addWindow(self,func):
		self.windows.append(func)
	def render(self):
		#this function returns a string that represents the gui renderd as text
		ret_val = 'guiId-' + str(self.Id) + ':' + '\n' + '-'*20 + '\n\n'
		for window in self.windows:
			w_txt = window(self)
			for line in w_txt.split('\n'):
				ret_val += '\t' + line + '\n'
			ret_val += '\n'
			ret_val += '-'*20 + '\n\n'
		return ret_val
	async def add(self,ctx):
		#this function adds a COPY of this gui to the system and sends
		#it to discord to render	
		g = copy.copy(self)
		g.Id = gui.getUniqId()
		gui.gui_arr.append(g)
	
		msg = await ctx.send(g.render())
		for emoji in g.emojiL:
			await msg.add_reaction(emoji)

async def checkGui(clientId,reaction,user):
	#this function is ment to be run in the addReaction event
	#in discord.py

	print('COUNT ' + str(reaction.count))
	if reaction.message.author.id == clientId and user.id != clientId:
		#the message was made by us and we did not create the reaction event
		#which means this is a valid message to check
 
		print('[*] I made that message!')

		#this is the syntax that this if statement is looking for
		#guiId-<id>:<poll description>		
		split_m = reaction.message.content.split(':')
		if len(split_m[0]) > 6 and len(split_m) > 1 and split_m[0].split('-')[0] == 'guiId' and len(split_m[0]) > 1:
			#we have a valid gui
			
			#attempt to parse out the gui Id
			try:
				Id = int(split_m[0].split('-')[1])
			except:
				print('[DGui] ERROR: invalid gui numeric found!')
				return False

			#attempt to parse out correct gui
			g = gui.getGuiId(Id)
			if g == None:
				print('[DGui] ERROR: invalid gui Id found!')
				return False	
			
			#update the poll

			#TODO: need to update every message in the cache that changes so all polls are up to date
			if reaction.count > 1:
				await reaction.message.remove_reaction(reaction.emoji,user)
			#TODO: add a reaciton removal system await reaction.message.remove_reaction(reaction.emoji,'a')
			ret_val = g.view()
			#now change behavior based on ret_val
			if ret_val == None:
				print('[DGui] ERROR: unkown view error!')
				return False
			await reaction.message.edit(content=str(g.update))
			
		#print(p.votes)
		#print(reaction.message.content)
			
if __name__ == '__main__':
	g = gui(['🐵'])
	#FUTURE TODO: make it so that the window functions have tags so you can target and delete one
	def hello_world(gui):
		return 'hello\nworld'
	def guiId(gui):
		return 'The gui id is ' + str(gui.Id)
	g.addWindow(hello_world)
	g.addWindow(guiId)

	print(g.render())
	
	bot = commands.Bot(command_prefix='test ')
	
	@bot.command()
	async def potato(ctx,*args):
		await g.add(ctx)
	bot.run('NTkwODg3MzU3NDE5MzU2MTcx.XQoyew.AKnkwp6Tar3MnUvK8vGYw9eEU_I')


	#we need to find a way to allow ppl to chose with reactions
