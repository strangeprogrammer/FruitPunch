#!/bin/python3

import pygame as pg

import menu

def main():
	pg.init()
	screen = pg.display.set_mode()
	
	menu.init()
	
	while True:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				pg.quit()
				return
			elif e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
				for i in menu.curMenu:
					if i.rect.collidepoint(e.pos):
						i.click()
		
		screen.fill( (255, 255, 255) )
		menu.curMenu.draw(screen)
		pg.display.flip()

main()
