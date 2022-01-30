import pygame
pygame.init()

import world as w
world = w.World()
world.init()

import render as r
r.world=world
r.renderInit()

import events as ev
while ev.running:
	for event in pygame.event.get():
		ev.event(event)
    
