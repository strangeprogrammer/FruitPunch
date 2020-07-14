#!/bin/python3

import pygame as pg

def main():
	pg.init()
	
	screen = pg.display.set_mode()
	defont = pg.font.Font(pg.font.get_default_font(), 200)
	text = defont.render("Hello, world!", True, (0, 0, 0) )
	
	screen.fill( (255, 255, 255) )
	screen.blit(text, (100, 100) )
	
	pg.display.flip()
	
	input()

main()
