#!/bin/python3

# Copyright (C) 2020 Stephen Fedele <32551324+strangeprogrammer@users.noreply.github.com>
# 
# This file is part of Fruit Punch.
# 
# Fruit Punch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Fruit Punch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Fruit Punch.  If not, see <https://www.gnu.org/licenses/>.
# 
# Additional terms apply to this file.  Read the file 'LICENSE.txt' for
# more information.



import pygame as pg
from pygame.sprite import LayeredUpdates as LU
from pygame.image import load as LD

import math

from physbodies import *

class wobble(baseBody):
	def __init__(self, *args, origCenter = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.origCenter = origCenter or self.rect.center
		self.rect.center = self.origCenter
	
	def update(self, t, *args):
		self.rect.centerx = self.origCenter[0] + math.sin(t) * 64
		super().update(t, *args)

class A(wobble): pass

class B(flipBody, wobble):
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

class C(rotationBody, wobble):
	def update(self, t, *args):
		self.theta = math.sin(t) * math.pi / 4
		
		super().update(t, *args)

class D(fullBody, wobble):
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
	a = A(image = LD("../RESOURCES/0.png"), origCenter = (250, 200))
	b = B(image = LD("../RESOURCES/1.png"), origCenter = (500, 300))
	c = C(image = LD("../RESOURCES/2.png"), origCenter = (750, 400))
	d = D(image = LD("../RESOURCES/3.png"), origCenter = (1000, 500))
	
	e = translationStrut(image = LD("../RESOURCES/4.png"), rel = a, xoffset = -64, yoffset = -64)
	f = flipStrut(image = LD("../RESOURCES/5.png"), rel = b, xoffset = -64, yoffset = -64)
	g = rotationStrut(image = LD("../RESOURCES/6.png"), rel = c, xoffset = -64, yoffset = -64)
	h = fullStrut(image = LD("../RESOURCES/7.png"), rel = d, xoffset = -64, yoffset = -64)
	
	return LU(a, b, c, d, e, f, g, h)
