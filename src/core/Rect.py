#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from .Crack import crack

class Rect(pg.Rect):
	def __add__(self, other):
		return Rect(
			self.left + other.left,
			self.top + other.top,
			self.width,
			self.height,
		)
	
	def __sub__(self, other):
		return Rect(
			self.left - other.left,
			self.top - other.top,
			self.width,
			self.height,
		)
