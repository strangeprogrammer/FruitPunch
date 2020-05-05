#!/bin/python3

import pygame

from pygame.sprite import Sprite, Group

class handoffRender(Group):
	"""Not optimized to remember old, affected regions (but,
	then again, it doesn't need to since (I plea to you) it
	should only be used with other Groups or Sprites that
	clean up after themselves)."""
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
