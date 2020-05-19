#!/bin/python3

import pygame as pg
from pygame.sprite import LayeredUpdates as LU

from newPlayer import newPlayer

keyDHandles = {}
keyUHandles = {}
playerActions = []

def quitProg():
	pg.quit()
	quit()

def keyDown(key):
	global keyDHandles
	keyDHandles.get(key, lambda: None)()

def keyUp(key):
	global keyUHandles
	keyUHandles.get(key, lambda: None)()

def handleEvent(e):
	if e.type == pg.QUIT:
		quitProg()
	elif e.type == pg.KEYDOWN:
		keyDown(e.key)
	elif e.type == pg.KEYUP:
		keyUp(e.key)

def init():
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	pg.display.flip()
	
	player = newPlayer()
	
	global keyUHandles
	global keyDHandles
	global playerActions
	keyDHandles[pg.K_a] = lambda: playerActions.append("RDown")
	keyUHandles[pg.K_a] = lambda: playerActions.append("RUp")
	keyDHandles[pg.K_s] = lambda: playerActions.append("BDown")
	keyUHandles[pg.K_s] = lambda: playerActions.append("BUp")
	keyDHandles[pg.K_d] = lambda: playerActions.append("GDown")
	keyUHandles[pg.K_d] = lambda: playerActions.append("GUp")
	keyDHandles[pg.K_f] = lambda: playerActions.append("YDown")
	keyUHandles[pg.K_f] = lambda: playerActions.append("YUp")
	
	return (screen, player, screen.copy())

def progBody(screen, player, bgd):
	list(map(handleEvent, pg.event.get())) # Must be forced out of laziness with 'list'
	
	global playerActions
	player.update(actions = playerActions, worldTime = pg.time.get_ticks())
	
	pg.display.update(player.draw(screen))
	player.clear(screen, bgd)
	
	playerActions.clear()

def main():
	pg.init()
	
	state = init()
	while True:
		progBody(*state)

main()
