#!/bin/python3

import pygame as pg

eventHandles = {}
systems = {}
allSprites = None
clock = pg.time.Clock()
screen = None
bgd = None

def cleanQuit():
	pg.quit()
	import sys
	sys.exit(0)

def processEvents():
	global eventHandles
	for e in pg.event.get():
		eventHandles.get(e.type, lambda: None)()

def mainLoop():
	processEvents()
	
	time = pg.time.get_ticks()
	
	global systems
	systems["ContAnimSystem"].update(time)
	
	global screen, bgd
	pg.display.update(systems["DrawSystem"].draw(screen))
	systems["DrawSystem"].clear(screen, bgd)
	
	global clock
	clock.tick(60)

def makeAll():
	global allSprites
	from makeSprites import makeSprites
	allSprites = makeSprites()
	
	global systems
	from DrawSystem import DrawSystem
	systems["DrawSystem"] = DrawSystem(allSprites.sprites())
	
	from ContAnimSystem import ContAnimSystem
	systems["ContAnimSystem"] = ContAnimSystem(allSprites.sprites())

def main():
	global screen, bgd
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	
	pg.display.flip()
	
	global eventHandles
	eventHandles[pg.QUIT] = cleanQuit
	
	makeAll()
	
	while True:
		mainLoop()

main()
