#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from System import System

class DrawSystem(System, pg.sprite.RenderUpdates):
	def clear(self, surface, bgd):
		super(System, self).clear(surface, bgd) # Run the pygame Group's 'clear' method
	
	def draw(self, surface):
		return super(System, self).draw(surface) # Run the pygame Group's 'draw' method
