import pygame
import numpy as np

world=0#placeholder, set in main.py

'''
showGrid=True
'''
showGrid=False
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

bgcolor=(50,50,50)
clrwhite=(255, 255, 255)

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
	xGridTotal=100*tileTotal
	yGridTotal=60*tileTotal
	
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
