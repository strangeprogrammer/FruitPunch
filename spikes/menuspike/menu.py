#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
from pygame.image import load as LD

curMenu = None

def init():
	RS = LD("./RESOURCES/RedSquare.png").convert_alpha()
	YS = LD("./RESOURCES/YellowSquare.png").convert_alpha()
	GS = LD("./RESOURCES/GreenSquare.png").convert_alpha()
	BS = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	PS = LD("./RESOURCES/PurpleSquare.png").convert_alpha()
	
	[
		menu1,
		menu2,
		menu3,
		menu4,
		menu5,
	] = [
		pg.sprite.Group(),
		pg.sprite.Group(),
		pg.sprite.Group(),
		pg.sprite.Group(),
		pg.sprite.Group()
	]
	
	menu1.add(menuitem(YS, topleft = (225, 100), menuLink = menu2))
	menu1.add(menuitem(GS, topleft = (350, 100), menuLink = menu3))
	
	menu2.add(menuitem(RS, topleft = (100, 225), menuLink = menu1))
	menu2.add(menuitem(GS, topleft = (350, 225), menuLink = menu3))
	menu2.add(menuitem(BS, topleft = (475, 225), menuLink = menu4))
	
	menu3.add(menuitem(RS, topleft = (100, 350), menuLink = menu1))
	menu3.add(menuitem(YS, topleft = (225, 350), menuLink = menu2))
	menu3.add(menuitem(PS, topleft = (600, 350), menuLink = menu5))
	
	menu4.add(menuitem(YS, topleft = (225, 475), menuLink = menu2))
	
	menu5.add(menuitem(GS, topleft = (350, 600), menuLink = menu3))
	
	global curMenu
	curMenu = menu3

class menuitem(pg.sprite.Sprite):
	def __init__(self, image, *args, topleft = None, menuLink = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.image = image
		
		self.rect = image.get_rect()
		if topleft is not None:
			self.rect.topleft = topleft
		
		self.menuLink = menuLink
	
	def click(self):
		global curMenu
		if self.menuLink is not None:
			curMenu = self.menuLink
