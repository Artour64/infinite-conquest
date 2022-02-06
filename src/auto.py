#!/usr/bin/python
import random
import render as r
import numpy as np
import pygame
#import world as w

claimTileCost=10

world=0#placeholder, set in main.py

relCords=[
		[1,1],
		[1,0],
		[1,-1],
		[-1,1],
		[-1,0],
		[-1,-1],
		[0,1],
		#[0,0],
		[0,-1]
	]

def tick():
	for c in world.empires:
		empireTick(c)
		print(str(len(c.tiles))+":"+str(c.getStash()))
	#print(world.empires[0].getStash())
	print("-----")
	r.renderTiles()
	pygame.display.update()

def transferTileResources(tileFrom,tileTo):
	if not tileFrom.hasTransfered:
		if tileFrom==tileTo:
			return
		tileTo.resources+=tileFrom.resources
		tileFrom.resources=0
		
		tileFrom.hasTransfered=True
		#prevent one turn lightning conveyor
		tileTo.hasTransfered=True
		

def tileProduce(tile):
	if tile.order==-1:
		if not tile.hasProduced:
			tile.resources+=1
			tile.hasProduced=True

def tileTurnReset(tile):
	tile.hasTransfered=False
	tile.hasProduced=False

def claimTile(tile,emp):
	if tile.resources>=claimTileCost:
		tile.resources-=claimTileCost
		tile.addToEmpire(emp)

	
def autoStash(emp):
	capCord=emp.capital
	#capTile=world.getTile(capCord)
	
	adjOwnedCords=adjacentOwnedCords(capCord,emp)
	adjStashTo=[]
	for c in adjOwnedCords:
		adjStashTo.append(capCord)
	while len(adjOwnedCords)>0:
		adjStashTo2=[]
		adjOwnedCords2=[]
		for c in range(len(adjOwnedCords)):
			adjacentEmptyCords=getTileAdjacentEmptyCords(adjOwnedCords[c],emp)
			tile=world.getTile(adjOwnedCords[c])
			if len(adjacentEmptyCords)==0:
				transferTileResources(tile,world.getTile(adjStashTo[c]))
				adj=adjacentOwnedCords(adjOwnedCords[c],emp)
				for q in adj:
					tile=world.getTile(q)
					if not tile.hasTransfered:
						if tile.order==-1:
							isIn=False
							for i in adjOwnedCords2:
								if i[0]==q[0]:
									if i[1]==q[1]:
										isIn=True
										break
							if not isIn:
								adjOwnedCords2.append(q)
								adjStashTo2.append(adjOwnedCords[c])
			else:
				autoExpandTile(tile,adjacentEmptyCords,emp)
		adjOwnedCords=adjOwnedCords2
		adjStashTo=adjStashTo2


def manhatanDist(a,b):
	return abs(a[0]-b[0])+abs(a[1]-b[1])

def diagDist(a,b):
	return max(abs(a[0]-b[0]),abs(a[1]-b[1]))
		
def autoExpandTile(tile,adjacentEmptyCords,emp):
	candidates=[0]
	adj=adjacentEmptyCords[0]
	res=world.getTile(adj).resources
	mDist=manhatanDist(adj,emp.capital)
	dDist=diagDist(adj,emp.capital)
	for i in range(1,len(adjacentEmptyCords)):
		adjCord=adjacentEmptyCords[i]
		adj=world.getTile(adjCord)
		if adj.resources > res:
			#new record
			candidates=[i]
			res=adj.resources
			mDist=manhatanDist(adjCord,emp.capital)
			dDist=diagDist(adjCord,emp.capital)
		elif adj.resources == res:#tie, next criteria
			mDist2=manhatanDist(adjCord,emp.capital)
			if  mDist2 < mDist:
				#new record
				candidates=[i]
				res=adj.resources
				mDist=mDist2
				dDist=diagDist(adjCord,emp.capital)
			elif mDist2 == mDist:#tie, next criteria
				dDist2=diagDist(adjCord,emp.capital)
				if  dDist2 < dDist:
					#new record
					candidates=[i]
					res=adj.resources
					mDist=mDist2
					dDist=dDist2
				else:#tie,add to list
					candidates.append(i)
	ind=random.choice(candidates)
	adj=adjacentEmptyCords[ind]
	to=world.getTile(adj)
	transferTileResources(tile,to)
	claimTile(to,emp)
	

def empireTick(emp):
	#tileTurnReset(capTile)
	for c in emp.tiles:
		tileTurnReset(c)
		tileProduce(c)
	#tileProduce(capTile)

	autoStash(emp)

def getTileAdjacentEmptyCords(cord,emp):
	cords=[]
	for c in relCords:
		adj=np.add(cord,c)
		tile=world.getTile(adj)
		if tile.own==-1:
			cords.append(adj)
	return cords

def adjacentOwnedCords(cord,emp):
	cords=[]
	for c in relCords:
		adj=np.add(cord,c)
		tile=world.getTile(adj)
		if tile.own==emp.id:
			if tile.order==-1:#auto
				cords.append(adj)
	return cords


#old, might scrap
def autoStash2(emp):
	capCord=emp.capital
	capTile=world.getTile(capCord)
	autoTransferTile(capCord,capTile,emp)

#old, might scrap
def autoTransferTile(cord,stashToTile,emp):
	tile=world.getTile(cord)
	if tile.hasTransfered:
		return
	#if tile.resources==0:
	#	return
	if tile.order!=-1:
		return
	adjacentEmptyCords=getTileAdjacentEmptyCords(cord,emp)
	if len(adjacentEmptyCords)==0:
		transferTileResources(tile,stashToTile)
		#recursive call
		adjOwned=adjacentOwnedCords(cord,emp)
		for c in adjOwned:
			tile2=world.getTile(c)
			if not tile2.hasTransfered:
				autoTransferTile(c,tile,emp)
	else:
		autoExpandTile(tile,adjacentEmptyCords,emp)

#might scrap
def tileTick(tile,emp):
	if tile.order==-1:#auto
		pass
	else:#manual order
		pass

#might scrap
def cordDistCompare(a,b,t):
	da=abs(a[0]-t[0])+abs(a[1]-t[1])
	db=abs(b[0]-t[0])+abs(b[1]-t[1])
	d=a-b
	if d!=0:
		if d>0:
			return 1
		else:
			return -1
	else:
		da=max(abs(a[0]-t[0]),abs(a[1]-t[1]))
		db=max(abs(b[0]-t[0]),abs(b[1]-t[1]))
		d=a-b
		if d>0:
			return 1
		elif d<0:
			return -1
		else:
			return 0
