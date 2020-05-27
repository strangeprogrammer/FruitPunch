#!/bin/python3

import pygame as pg

from makeBodies import makeBodies

def main():
	pg.init()
	
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	pg.display.flip()
	bodies = makeBodies()
	
	goflag = True
	while goflag:
		bodies.update(pg.time.get_ticks() / 1000)
		pg.display.update(bodies.draw(screen))
		bodies.clear(screen, bgd)
		
		for e in pg.event.get():
			if e.type == pg.QUIT:
				goflag = False
				break
	
	pg.quit()

main()
