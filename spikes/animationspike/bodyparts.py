#!/bin/python3

import pygame as pg
import math

from sprites import drawnSprite

class redComp(pg.sprite.DirtySprite):
	def __init__(self, rel, *args, **kwargs):
		self._rel = rel
		self.image = pg.image.load("./RedSquare.png")
		self.rect = self.image.get_rect()
		self._layer = 2
		super().__init__(*args, **kwargs)
	
	def update(self, time):
		rel = self._rel.rect
		self.rect.center = (rel.center[0], rel.center[1] + 96 * math.sin(time / 250))

class blueComp(pg.sprite.DirtySprite):
	def __init__(self, rel, *args, **kwargs):
		self._rel = rel
		self.image = pg.image.load("./BlueSquare.png")
		self.rect = self.image.get_rect()
		self._layer = 1
		super().__init__(*args, **kwargs)
	
	def update(self, time):
		rel = self._rel.rect
		self.rect.center = (rel.center[0] + 96 * math.sin((time + 3141) / 250), rel.center[1])

class greenComp(pg.sprite.DirtySprite):
	def __init__(self, *args, **kwargs):
		self.image = pg.image.load("./GreenSquare.png")
		self.rect = self.image.get_rect()
		self._layer = 0
		super().__init__(*args, **kwargs)

def basicBody(center):
	green = greenComp()
	green.rect.center = center
	
	red = redComp(green)
	blue = blueComp(green)
	
	return pg.sprite.LayeredUpdates(red, blue, green)
