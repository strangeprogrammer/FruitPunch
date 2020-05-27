#!/bin/python3

import pygame as pg
from pygame.sprite import LayeredUpdates as LU
from pygame.image import load as LD
import math

from bodies import *

class A(baseBody):
	def update(self, t):
		super().update()

class B(flipBody):
	def update(self, t):
		# Sequence: Flip y, Flip x, Flip y, Flip x (should be the grey code for all states)
		
		if t % math.tau < math.pi:
			self.flipx = False
		else:
			self.flipx = True
		
		if (t + math.pi / 2) % math.tau < math.pi:
			self.flipy = False
		else:
			self.flipy = True
		
		super().update()

class C(rotationBody):
	def update(self, t):
		self.theta = math.sin(t) * math.pi / 4
		
		super().update()

class D(fullBody):
	def update(self, t):
		if t % math.tau < math.pi:
			self.flipx = False
		else:
			self.flipx = True
		
		if (t + math.pi / 2) % math.tau < math.pi:
			self.flipy = False
		else:
			self.flipy = True
		
		self.theta = math.sin(t) * math.pi / 4
		
		super().update()

def makeBodies():
	a = A(image = LD("../RESOURCES/0.png"))
	a.rect.center = (100, 100)
	b = B(image = LD("../RESOURCES/1.png"))
	b.rect.center = (200, 200)
	c = C(image = LD("../RESOURCES/2.png"))
	c.rect.center = (300, 300)
	d = D(image = LD("../RESOURCES/3.png"))
	d.rect.center = (400, 400)
	
	return LU(a, b, c, d)
