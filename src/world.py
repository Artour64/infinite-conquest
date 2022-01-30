import random
import math

chunkSize=128

spawnX=4
spawnY=4
spawnsize=spawnX*spawnY

spawnEmpires=8

playerStartSize=25
empireSpawnMinSizeFactor=0.5
empireSpawnMaxSizeFactor=2

scaleFactor=4

sightRange=5

class Tile:
	def __init__(self):
		self.scale=1
		self.resources=0
		self.own=-1
		self.order=-1
		self.seen=False
		self.fog=True
		#self.subtiles=0

'''
class Chunk:
	def __init__(self):
		self.scale=1
		pass
	def init(self,cs=chunkSize):
		self.grid=[]
		for x in range(chunkSize):
			self.grid.append(list())
			for y in range(chunkSize):
				t=Tile()
				self.grid[x].append(t)
		return self
'''
	
class World:
	def __init__(self):
		self.turn=0
		self.scale=1
		self.empires=[]
	def init(self):
		self.grid=[]
		for x in range(chunkSize*spawnX):
			self.grid.append(list())
			for y in range(chunkSize*spawnY):
				t=Tile()
				self.grid[x].append(t)
		
		empDeck=[]
		for c in range(spawnEmpires):
			empDeck.append(c)
			self.empires.append(Empire())
		for c in range(spawnsize-spawnEmpires):
			empDeck.append(-1)
		random.shuffle(empDeck)
		self.empires[0].player=True
		
		for c in range(len(empDeck)):
			emp=empDeck[c]
			empSize=0
			if emp==-1:
				pass
			elif emp==0:#player
				empSize=playerStartSize
			else:#other empire
				empSizeMin=math.ceil(playerStartSize*empireSpawnMinSizeFactor)
				empSizeMax=math.floor(playerStartSize*empireSpawnMaxSizeFactor)
				if empSizeMin>=empSizeMax:
					empSize=empSizeMax
				else:
					empSize=random.randint(empSizeMin,empSizeMax)
			pass
			
			
class Empire:
	def __init__(self):
		self.scale=1
		self.player=False
