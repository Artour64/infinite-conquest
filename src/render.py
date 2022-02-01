import pygame
import numpy as np

#import world as w

world=0#placeholder, set in main.py

'''
showGrid=True
'''
showGrid=False
showGrid=True
#'''

tileSize=16
tileTotal=tileSize
if(showGrid):
	tileTotal+=1

#icon = pygame.image.load("snake-clip.png")
#pygame.display.set_icon(icon)
#screen.blit(icon, (50, 50))

#defaults as placeholders, set in renderInit() 
#xGridTotal=w.worldX*tileTotal
#yGridTotal=w.worldY*tileTotal
xGridTotal=10*tileTotal
yGridTotal=10*tileTotal

'''
sizebartop=50
sizebarbottom=50
sizebarleft=50
sizebarright=50
'''
sizebartop=0
sizebarbottom=0
sizebarleft=0
sizebarright=0
#'''

wc=(sizebarleft,sizebartop)
if(showGrid):
	to=np.add(wc,(1,1))
else:
	to=wc

screenX=xGridTotal+sizebarright+sizebarleft
screenY=yGridTotal+sizebartop+sizebarbottom
if(showGrid):
	screenX+=1
	screenY+=1

#icon = pygame.image.load("snake-clip.png")
#pygame.display.set_icon(icon)
#screen.blit(icon, (50, 50))

font = pygame.font.Font('freesansbold.ttf', 32)

#screen=pygame.display.set_mode((screenX, screenY))#placeholder, set in renderInit()

clrblack=(0,0,0)
bgcolor=(50,50,50)
clrwhite=(255, 255, 255)

clrGrid=bgcolor


empireColor=[
	(255,0,0),
	(0,255,0),
	(0,0,255),
	(0,255,255),
	(255,255,0),
	(255,0,255),
	(55,100,0),
	(100,55,0),
	(100,0,55),
	(55,0,100),
	(0,55,100),
	(0,100,55),
	(155,100,0),
	(100,155,0),
	(100,0,155),
	(155,0,100),
	(0,155,100),
	(0,100,155),	
	(100,0,0),
	(0,100,0),
	(0,0,100),
	(0,100,100),
	(100,100,0),
	(100,0,100),
	(255,100,100),
	(100,255,100),
	(100,100,255),
	#(100,255,255),
	#(255,255,100)
	#(255,100,255)
]

def renderInit():
	global tileTotal
	global xGridTotal
	global yGridTotal
	global wc
	global to
	global screenX
	global screenY
	global screen
	
	tileTotal=tileSize
	if(showGrid):
		tileTotal+=1
	
	#xGridTotal=world.worldX*tileTotal
	#yGridTotal=world.worldY*tileTotal
	#xGridTotal=100*tileTotal
	#yGridTotal=60*tileTotal
	
	xGridTotal=16*4*tileTotal
	yGridTotal=16*4*tileTotal
	
	wc=(sizebarleft,sizebartop)
	if(showGrid):
		to=np.add(wc,(1,1))
	else:
		to=wc

	screenX=xGridTotal+sizebarright+sizebarleft
	screenY=yGridTotal+sizebartop+sizebarbottom
	if(showGrid):
		screenX+=1
		screenY+=1
	
	screen = pygame.display.set_mode((screenX, screenY))
	pygame.display.set_caption("Infinite Conquest")
	renderTiles()
	renderGridBorder()
	pygame.display.update()
	
def renderTiles():
	for x in range(len(world.grid)):#x is row
		for y in range(len(world.grid[0])):#y is tile
			renderCordTile([x,y])

def renderCordTile(t):
	tile=world.grid[t[0]][t[1]]
	cord=(t[0], t[1])
	cord=np.multiply(tileTotal,cord)
	cord=np.add(to,cord)
	if tile.own==-1:
		pygame.draw.rect(screen, clrblack, pygame.Rect(cord[0], cord[1], tileSize, tileSize))
	elif tile.own==-2:#divided?
		pass
	elif tile.capital:
		pygame.draw.rect(screen, clrwhite, pygame.Rect(cord[0], cord[1], tileSize, tileSize))
	else:
		pygame.draw.rect(screen, empireColor[world.empires[tile.own].color], pygame.Rect(cord[0], cord[1], tileSize, tileSize))
	
	
def renderGridBorder():
	for x in range(16*4):
		pygame.draw.line(screen,clrGrid,np.add(wc,(x*tileTotal,0)),np.add(wc,(x*tileTotal,yGridTotal)),1)
	for y in range(16*4):
		pygame.draw.line(screen,clrGrid,np.add(wc,(0,y*tileTotal)),np.add(wc,(xGridTotal,y*tileTotal)),1)
	pygame.draw.line(screen,clrGrid,np.add(wc,(0,yGridTotal)),np.add(wc,(xGridTotal,yGridTotal)),1)
	pygame.draw.line(screen,clrGrid,np.add(wc,(xGridTotal,0)),np.add(wc,(xGridTotal,yGridTotal)),1)

