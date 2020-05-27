#!/bin/python3

import pygame
import math

from bodyparts import basicBody

def makeBodies():
	x = basicBody((500, 500))
	y = basicBody((700, 300))
	return [x, y]

def updateBodies(bodies, *args):
	for group in bodies:
		group.update(*args)

def drawBodies(bodies, surface):
	rects = []
	for group in bodies:
		rects += group.draw(surface)
	return rects

def clearBodies(bodies, surface, bgd):
	for group in bodies:
		group.clear(surface, bgd)

def main():
	pygame.init()
	
	screen = pygame.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	pygame.display.flip()
	bodies = makeBodies()
	
	goflag = True
	while goflag:
		updateBodies(bodies, pygame.time.get_ticks())
		pygame.display.update(drawBodies(bodies, screen))
		clearBodies(bodies, screen, bgd)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				goflag = False
				break
	
	pygame.quit()

main()
