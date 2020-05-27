#!/bin/python3

import pygame as pg
from sys import exit

handlers = {}
keyDownHandlers = {}
clock = None
screen = None
bgd = None
player = None
drawables = None
velStep = 0.05

def handleQuit(e):
	pg.quit()
	exit(0)

def goUp(player):
	global velStep
	player.velocity[1] -= velStep

def goDown(player):
	global velStep
	player.velocity[1] += velStep

def goLeft(player):
	global velStep
	player.velocity[0] -= velStep

def goRight(player):
	global velStep
	player.velocity[0] += velStep

def handleKeyDown(e):
	global keyDownHandlers
	handle = keyDownHandlers.get(e.key, lambda x: None)
	handle(e)

def doEvents():
	for e in pg.event.get():
		global handlers
		handle = handlers.get(e.type, lambda x: None)
		handle(e)

from makePlayer import makePlayer

def init():
	global handlers, keyDownHandlers, clock, screen, bgd, player, drawables
	
	handlers[pg.QUIT] = handleQuit
	handlers[pg.KEYDOWN] = handleKeyDown
	
	keyDownHandlers[pg.K_UP]	= lambda e: goUp(player)
	keyDownHandlers[pg.K_DOWN]	= lambda e: goDown(player)
	keyDownHandlers[pg.K_LEFT]	= lambda e: goLeft(player)
	keyDownHandlers[pg.K_RIGHT]	= lambda e: goRight(player)
	
	clock = pg.time.Clock()
	
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	
	bgd = screen.copy()
	
	player = makePlayer()
	
	drawables = pg.sprite.LayeredUpdates(player)

def update():
	global clock, screen, bgd, player, drawables
	
	clock.tick(60)
	
	doEvents()
	
	player.update(clock.get_time())
	
	drawables.draw(screen)
	
	# pg.display.update(<BOXES>)
	pg.display.flip()
	
	drawables.clear(screen, bgd)

def main():
	init()
	
	while True:
		update()

main()
