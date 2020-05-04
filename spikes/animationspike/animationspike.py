#!/bin/python3

import pygame
import math

from bodyparts import basicBody

def makeSprites():
	x = basicBody((500, 500))
	y = basicBody((700, 300))
	return pygame.sprite.Group(x, y)

def drawBodies(group, surface):
	rects = []
	for sprite in group:
		rects += sprite.draw(surface)
	return rects

def clearBodies(group, surface, bgd):
	for sprite in group:
		sprite.clear(surface, bgd)

def main():
	pygame.init()
	
	screen = pygame.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	pygame.display.flip()
	sprites = makeSprites()
	
	goflag = True
	while goflag:
		sprites.update(pygame.time.get_ticks())
		pygame.display.update(drawBodies(sprites, screen))
		clearBodies(sprites, screen, bgd)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				goflag = False
				break
	
	pygame.quit()

main()
