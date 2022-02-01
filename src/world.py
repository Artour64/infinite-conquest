import random
import math
import render as r

chunkSize=16

spawnX=4
spawnY=4
spawnsize=spawnX*spawnY

spawnEmpires=8

playerStartSize=25
empireSpawnMinSizeFactor=0.5
empireSpawnMaxSizeFactor=2

scaleFactor=4

sightRange=5

playerColor=0

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
		
		#turn dynamic variables
		self.hasProduced=False
		self.hasTransfered=False
		
		#self.visChange=False
		
		#self.transferToDist=0
		
	def addToEmpire(self,emp):
		self.own=emp.id
		if emp.player:
			self.seen=True
		emp.tiles.append(self)
		
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
	
	def getTile(self,cord):
		return self.grid[cord[0]][cord[1]]
	
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
			empire=Empire()
			self.empires.append(empire)
			empire.id=c
			empire.world=self
		for c in range(spawnsize-spawnEmpires):
			empDeck.append(-1)
		random.shuffle(empDeck)
		self.empires[0].player=True
		
		empColor=list(range(len(r.empireColor)))
		random.shuffle(empColor)
		self.empires[0].color=playerColor
		for c in range(1,len(self.empires)):
			if empColor[c]==playerColor:
				self.empires[c].color=empColor[0]
			else:
				self.empires[c].color=empColor[c]

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
				emp=self.empires[emp]
				for x in range(empLength):
					for y in range(empLength):
						tile=self.grid[posx+x][posy+y]
						tile.addToEmpire(emp)
				emp.capital=[posx+math.floor(empLength/2),posy+math.floor(empLength/2)]
				tile=self.grid[posx+math.floor(empLength/2)][posy+math.floor(empLength/2)]
				tile.capital=True
				empRemainSide=math.floor(empRemain/4)
				empRemainSideRemain=empRemain%4
				dev=0
				remSide=1
				while empRemainSide>0:
					tile=self.grid[posx-1][posy+math.floor(empLength/2)+(dev*remSide)]
					tile.addToEmpire(emp)
					tile=self.grid[posx+empLength][posy+math.floor(empLength/2)-(dev*remSide)]
					tile.addToEmpire(emp)
					tile=self.grid[posx+math.floor(empLength/2)+(dev*remSide)][posy-1]
					tile.addToEmpire(emp)
					tile=self.grid[posx+math.floor(empLength/2)-(dev*remSide)][posy+empLength]
					tile.addToEmpire(emp)
					
					if remSide==1:
						dev+=1
					remSide*=-1
					empRemainSide-=1
					
				
				if empRemainSideRemain>0:
					tile=self.grid[posx-1][posy+math.floor(empLength/2)+(dev*remSide)]
					tile.addToEmpire(emp)
					empRemainSideRemain-=1
				elif empRemainSideRemain>0:
					tile=self.grid[posx+empLength][posy+math.floor(empLength/2)-(dev*remSide)]
					tile.addToEmpire(emp)
					empRemainSideRemain-=1
				elif empRemainSideRemain>0:
					tile=self.grid[posx+math.floor(empLength/2)+(dev*remSide)][posy-1]
					tile.addToEmpire(emp)
					empRemainSideRemain-=1
				elif empRemainSideRemain>0:
					tile=self.grid[posx+math.floor(empLength/2)-(dev*remSide)][posy+empLength]
					tile.addToEmpire(emp)
				
			
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
		self.color=0
		self.tiles=[]
		self.orders=[]
		self.world=0
	
	def getStash(self):
		return self.world.getTile(self.capital).resources
