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
		self.fog=0#time since last observed
		self.capital=False
		self.subtiles=None
		self.supertile=None
		self.units=[]
		
class Unit:
	def __init__(self):
		self.scale=1
		self.resources=0
		self.own=-1
		self.order=-1

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
		self.player=0
		self.scale=1
		self.empires=[]
		self.units=[]
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
			self.empires[c].id=c
		for c in range(spawnsize-spawnEmpires):
			empDeck.append(-1)
		random.shuffle(empDeck)
		self.empires[0].player=True
		
		for c in range(len(empDeck)):
			emp=empDeck[c]
			if emp==-1:
				continue
			empSize=0
			if emp==0:#player
				empSize=playerStartSize
			else:#other empire
				empSizeMin=math.ceil(playerStartSize*empireSpawnMinSizeFactor)
				empSizeMax=math.floor(playerStartSize*empireSpawnMaxSizeFactor)
				if empSizeMin>=empSizeMax:
					empSize=empSizeMax
				else:
					empSize=random.randint(empSizeMin,empSizeMax)
			empLength=math.floor(math.sqrt(empSize))
			if empLength % 2 == 0:#odd square root,
				empLength-=1#force odd so that capital is in the middle
			empRemain=empSize-(empLength*empLength)
			chunkx= (c % spawnX)*chunkSize
			chunky= math.floor(c / spawnX)*chunkSize
			if empLength+2<=chunkSize:#empire spawned fits in chunk
				posx=random.randint(0,chunkSize-(empLength+2))+1+chunkx
				posy=random.randint(0,chunkSize-(empLength+2))+1+chunky
				for x in range(empLength):
					for y in range(empLength):
						tile=self.grid[posx+x][posy+y]
						tile.own=emp
						tile.seen=True
				self.empires[emp].capital=[posx+math.ceil(empLength/2),posy+math.ceil(empLength/2)]
				tile=self.grid[posx+math.ceil(empLength/2)][posy+math.ceil(empLength/2)]
				tile.capital=True
				empRemainSide=math.floor(empRemain/4)
				empRemainSideRemain=empRemain%4
				dev=0
				remSide=-1
				while empRemainSide>0:
					tile=self.grid[posx-1][posy+math.ceil(empLength/2)+(dev*remSide)]
					tile.own=emp
					tile.seen=True
					tile=self.grid[posx+1+empLength][posy+math.ceil(empLength/2)+(dev*remSide)]
					tile.own=emp
					tile.seen=True
					tile=self.grid[posx+math.ceil(empLength/2)+(dev*remSide)][posy-1]
					tile.own=emp
					tile.seen=True
					tile=self.grid[posx+math.ceil(empLength/2)+(dev*remSide)][posy+1+empLength]
					tile.own=emp
					tile.seen=True
					
					remSide*=-1
					empRemainSide-=1
					dev+=1
					
				if empRemainSideRemain>0:
					tile=self.grid[posx-1][posy+math.ceil(empLength/2)+(dev*remSide)]
					tile.own=emp
					tile.seen=True
					empRemainSideRemain-=1
				elif empRemainSideRemain>0:
					tile=self.grid[posx+1+empLength][posy+math.ceil(empLength/2)+(dev*remSide)]
					tile.own=emp
					tile.seen=True
					empRemainSideRemain-=1
				elif empRemainSideRemain>0:
					tile=self.grid[posx+math.ceil(empLength/2)+(dev*remSide)][posy-1]
					tile.own=emp
					tile.seen=True
					empRemainSideRemain-=1
				elif empRemainSideRemain>0:
					tile=self.grid[posx+math.ceil(empLength/2)+(dev*remSide)][posy+1+empLength]
					tile.own=emp
					tile.seen=True
			
			#todo:
			elif empSize<chunkSize*chunkSize:#empire spawned fits in chunk but just barely
				pass
			else:#empire spawned does not fit in chunk (or uses exactly the entire chunk)
				pass
			
			
class Empire:
	def __init__(self):
		self.scale=1
		self.player=False
		self.id=-1
		self.units=[]
		self.capital=[0,0]
