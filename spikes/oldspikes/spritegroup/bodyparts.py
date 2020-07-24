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
