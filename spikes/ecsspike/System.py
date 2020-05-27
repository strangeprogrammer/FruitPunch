#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from abc import ABC, abstractmethod

class System(ABC, pg.sprite.Group):
	# Pygame Groups are nice, but there are some things we don't need from them
	def clear(self, *args, **kwargs):
		pass
	
	# Pygame Groups are nice, but there are some things we don't need from them
	def draw(self, *args, **kwargs):
		pass
