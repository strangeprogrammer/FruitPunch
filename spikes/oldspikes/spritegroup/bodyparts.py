#!/bin/python3

import pygame
import math

import SG

class bodyComponent(pygame.sprite.DirtySprite):
	def __init__(self, rel, path, *args, layer = 0):
		self._rel = rel
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self._layer = layer
		super().__init__(*args)

class redComp(bodyComponent):
	def __init__(self, rel, *args):
		super().__init__(rel, "./RedSquare.png", *args, layer = 2)
	
	def update(self, time):
		rel = self._rel.rect
		self.rect.center = (rel.center[0], rel.center[1] + 96 * math.sin(time / 250))

class blueComp(bodyComponent):
	def __init__(self, rel, *args):
		super().__init__(rel, "./BlueSquare.png", *args, layer = 1)
	
	def update(self, time):
		rel = self._rel.rect
		self.rect.center = (rel.center[0] + 96 * math.sin((time + 3141) / 250), rel.center[1])

class greenComp(bodyComponent):
	def __init__(self, *args):
		super().__init__(None, "./GreenSquare.png", *args, layer = 0)

def basicBody(center):
	green = greenComp()
	green.rect.center = center
	
	red = redComp(green)
	blue = blueComp(green)
	
	return SG.LayeredSG(sprites = [red, blue, green])
