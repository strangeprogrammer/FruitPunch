#!/bin/python3

import pygame as pg
import math

class baseBody(pg.sprite.DirtySprite):
	"""A thin sprite wrapper for an image, its rectangle, and its layer."""
	
	def __init__(self, *args, image = None, rect = None, layer = 0, **kwargs):
		super().__init__(*args, **kwargs)
		if image is None:
			raise Exception() # Must be passed an image
		if rect is None:
			rect = image.get_rect()
		self.origImage = self.image = image
		self.rect = rect
		self._layer = layer
	
	def update(self, *args): # Preserves the center of the rect across updates (so that we don't have to implicity rely upon 'translationStrut' all the time)
		oldCenter = self.rect.center
		(self.image, self.rect) = self._body()
		self.rect.center = oldCenter
	
	def _body(self, origImage = None, **kwargs):
		origImage = origImage or self.origImage
		return (origImage, origImage.get_rect())

class flipBody(baseBody):
	"""A sprite that keeps track of how it's flipped."""
	
	def __init__(self, *args, flipx = False, flipy = False, **kwargs):
		super().__init__(*args, **kwargs)
		self.postFlip = self.origImage
		self._flipx = flipx
		self._flipy = flipy
		self._dirtyFlip = True
	
	def _body(self, origImage = None, flipx = None, flipy = None, **kwargs):
		origImage = origImage or self.origImage
		flipx = flipx or self._flipx
		flipy = flipy or self._flipy
		
		if self._dirtyFlip:
			if flipx or flipy:
				image = pg.transform.flip(origImage, flipx, flipy)
			else:
				image = origImage
		else:
			image = self.postFlip
			
		self.postFlip = image
		self._dirtyFlip = False
		return super()._body(origImage = image, **kwargs)
	
	@property
	def flipx(self):
		return self._flipx
	
	@flipx.setter
	def flipx(self, b):
		if self._flipx != b:
			self._flipx = b
			self._dirtyFlip = True
	
	@property
	def flipy(self):
		return self._flipy
	
	@flipy.setter
	def flipy(self, b):
		if self._flipy != b:
			self._flipy = b
			self._dirtyFlip = True
	
	@property
	def singleFlip(self):
		return bool(self._flipx) ^ bool(self._flipy)

class rotationBody(baseBody):
	"""A sprite that keeps track of its rotation."""
	
	def __init__(self, *args, theta = 0, **kwargs):
		super().__init__(*args, **kwargs)
		self._theta = theta
	
	def _body(self, origImage = None, theta = None, **kwargs):
		origImage = origImage or self.origImage
		theta = theta or self._theta
		image = pg.transform.rotate(origImage, theta * 360 / math.tau)
		return super()._body(origImage = image, **kwargs)
	
	@property
	def theta(self):
		return self._theta
	
	@theta.setter
	def theta(self, angle):
		self._theta = angle

class fullBody(flipBody, rotationBody):
	"""A sprite that keeps track of its flipping state and rotation."""
	# We do not reverse the angle when the image is only flipped 1 way in order to make programming easier
	
	pass
