#!/bin/python3

import pygame as pg
import math

from bodyparts import basicBody
import SG

def makeBodies():
	x = basicBody((500, 500))
	y = basicBody((700, 300))
	return SG.handoffRender(x, y)

def main():
	pg.init()
	
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	pg.display.flip()
	bodies = makeBodies()
	
	goflag = True
	while goflag:
		bodies.update(pg.time.get_ticks())
		pg.display.update(bodies.draw(screen))
		bodies.clear(screen, bgd)
		for e in pg.event.get():
			if e.type == pg.QUIT:
				goflag = False
				break
	
	pg.quit()

main()
