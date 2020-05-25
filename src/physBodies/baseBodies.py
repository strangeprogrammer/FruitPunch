#!/bin/python3

import pygame as pg

class baseBody(pg.sprite.DirtySprite):
	"""A thin sprite wrapper for an image, its rectangle, and its layer."""
	
	def __init__(self, *args, image = None, rect = None, layer = 0, center = None, **kwargs):
		super().__init__(*args, **kwargs)
		
		if image is None:
			raise Exception() # Must be passed an image
		self.origImage = self.image = image
		
		rect = rect or image.get_rect()
		self.center = list(center or rect.center) # We must have an independent notion of the center since it could be a float instead of an integer number of pixels
		rect.center = tuple(map(int, self.center))
		self.rect = rect
		
		self._layer = layer
	
	def update(self, *args): # Preserves the center of the rect across updates (so that we don't have to implicity rely upon 'translationStrut' all the time)
		oldCenter = self.center
		(self.image, self.rect) = self._body()
		self.center = oldCenter
		self.rect.center = tuple(map(int, self.center))
	
	def _body(self, origImage = None, **kwargs):
		origImage = origImage or self.origImage
		return (origImage, origImage.get_rect())

class relBody(baseBody):
	def __init__(self, *args, rel = None, **kwargs):
		super().__init__(*args, **kwargs)
		if rel is None:
			raise Exception() # Must be passed a relative sprite
		self.rel = rel
