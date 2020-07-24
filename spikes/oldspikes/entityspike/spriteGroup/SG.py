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

from pygame.sprite import Sprite, Group

class handoffRender(Group):
	"""Not optimized to remember old, affected regions (but,
	then again, it doesn't need to be since (I plea to you)
	it should only be used with other Sprites or
	SpriteGroups that clean up after themselves)."""
	
	def draw(self, surface):
		rectangles = []
		for sprite in self.sprites():
			r = sprite.draw(surface)
			if r is not None:
				rectangles += r
		return rectangles
	
	def clear(self, surface, bgd):
		for sprite in self.sprites():
			sprite.clear(surface, bgd)

class spriteGroup(Sprite):
	def __init__(self, *groups, container = None, sprites = []):
		self.container = container(*sprites) or Group(*sprites)
		super().__init__(*groups)
	
	def update(self, *args, **kwargs):
		return self.container.update(*args, **kwargs)
	
	def draw(self, surface):
		return self.container.draw(surface)
	
	def clear(self, surface, bgd):
		return self.container.clear(surface, bgd)

class LayeredSG(spriteGroup):
	def __init__(self, *groups, sprites = []):
		super().__init__(*groups, container = pygame.sprite.LayeredUpdates, sprites = sprites)

class handoffSG(spriteGroup):
	def __init__(self, *groups, sprites = []):
		super().__init__(*groups, container = handoffRender, sprites = sprites)
