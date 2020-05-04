#!/bin/python3

import pygame
import math

from sprites import drawnSprite, layerSprite

class redComp(layerSprite):
	def __init__(self, rel, *args, **kwargs):
		self._rel = rel
		image = pygame.image.load("./RedSquare.png")
		super().__init__(image, image.get_rect(), *args, layer = 2, **kwargs)
	
	def update(self, time):
		rel = self._rel.get_rect()
		self.rect.center = (rel.center[0], rel.center[1] + 96 * math.sin(time / 250))

class blueComp(layerSprite):
	def __init__(self, rel, *args, **kwargs):
		self._rel = rel
		image = pygame.image.load("./BlueSquare.png")
		super().__init__(image, image.get_rect(), *args, layer = 1, **kwargs)
	
	def update(self, time):
		rel = self._rel.get_rect()
		self.rect.center = (rel.center[0] + 96 * math.sin((time + 3141) / 250), rel.center[1])

class basicBody(drawnSprite, pygame.sprite.Sprite):
	def __init__(self, center, *args, **kwargs):
		refSprite = layerSprite.initPath("./GreenSquare.png")
		refSprite.get_rect().center = center
		
		red = redComp(refSprite)
		blue = blueComp(refSprite)
		
		self._allsprites = pygame.sprite.LayeredUpdates(refSprite, red, blue)
		super().__init__(*args, **kwargs)
	
	def update(self, *args):
		self._allsprites.update(*args)
	
	def draw(self, surface):
		return self._allsprites.draw(surface)
	
	def clear(self, surface, bgd):
		self._allsprites.clear(surface, bgd)
