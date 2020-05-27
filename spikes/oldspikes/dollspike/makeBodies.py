#!/bin/python3

import pygame as pg
from pygame.sprite import LayeredUpdates as LU
from pygame.image import load as LD

import math

from physbodies import *

class wobble(baseBody):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.origCenter = self.rect.center
	
	def update(self, t, *args):
		self.rect.centerx = self.origCenter[0] + math.sin(t) * 64
		super().update(t, *args)

class A(flipBody, wobble):
	def update(self, t, *args):
		# Sequence: Flip y, Flip x, Flip y, Flip x (should be the grey code for all states)
		
		if t % math.tau < math.pi:
			self.flipx = False
		else:
			self.flipx = True
		
		if (t + math.pi / 2) % math.tau < math.pi:
			self.flipy = False
		else:
			self.flipy = True
		
		super().update(t, *args)

class B(rotationBody, wobble):
	def update(self, t, *args):
		self.theta = math.sin(t) * math.pi / 4
		
		super().update(t, *args)

class C(fullBody, wobble):
	def update(self, t, *args):
		if t % math.tau < math.pi:
			self.flipx = False
		else:
			self.flipx = True
		
		if (t + math.pi / 2) % math.tau < math.pi:
			self.flipy = False
		else:
			self.flipy = True
		
		self.theta = math.sin(t) * math.pi / 4
		
		super().update(t, *args)

def makeBodies():
	a = A(image = LD("../RESOURCES/0.png"), center = (250, 200))
	b = B(image = LD("../RESOURCES/1.png"), center = (500, 200))
	c = C(image = LD("../RESOURCES/2.png"), center = (750, 200))
	
	d = flipDoll(image = LD("../RESOURCES/3.png"), rel = a, center = (250, 300))
	e = rotationDoll(image = LD("../RESOURCES/4.png"), rel = b, center = (500, 300))
	f = fullDoll(image = LD("../RESOURCES/5.png"), rel = c, center = (750, 300))
	
	return LU(a, b, c, d, e, f)
