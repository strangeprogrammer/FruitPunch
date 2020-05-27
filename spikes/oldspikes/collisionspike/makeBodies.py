#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from physBodies.velocity import velocityBody
from physBodies.collide import collideBody

class toggleImage(collideBody):
	def __init__(self, *args, alt1 = None, alt2 = None, **kwargs):
		super().__init__(*args, **kwargs)
		
		if alt1 is None:
			raise Exception() # Must be passed an image
		self.alt1 = alt1
		
		if alt2 is None:
			raise Exception() # Must be passed an image
		self.alt2 = alt2
		
		self.origorig = self.origImage
		self.collisionCount = 0
		self._decidePicture()
	
	def _decidePicture(self):
		if self.collisionCount == 0:
			self.origImage = self.origorig
		elif self.collisionCount == 1:
			self.origImage = self.alt1
		elif self.collisionCount == 2:
			self.origImage = self.alt2
	
	def onCollide(self, other):
		self.collisionCount += 1
		self._decidePicture()
	
	def offCollide(self, other):
		self.collisionCount -= 1
		self._decidePicture()

def makeBodies(clock):
	from pygame.image import load as LD
	
	orig = LD("../RESOURCES/GreenSquare.png")
	alt1 = LD("../RESOURCES/BlueSquare.png")
	alt2 = LD("../RESOURCES/YellowSquare.png")
	
	a = velocityBody(image = LD("../RESOURCES/0.png"), layer = 1, center = (400, 600), clock = clock, velocity = (0, 0))
	b = velocityBody(image = LD("../RESOURCES/1.png"), layer = 1, center = (600, 600), clock = clock, velocity = (0, 0))
	c = pg.sprite.Group(
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (200, 200)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (400, 200)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (600, 200)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (800, 200)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (200, 400)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (400, 400)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (600, 400)),
		toggleImage(image = orig, alt1 = alt1, alt2 = alt2, layer = 0, center = (800, 400)),
	)
	return (a, b, c)
