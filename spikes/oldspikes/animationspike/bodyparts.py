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
