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

### Bodies

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

### Related Bodies

class relBody():
	def __init__(self, *args, rel = None, **kwargs):
		super().__init__(*args, **kwargs)
		if rel is None:
			raise Exception() # Must be passed a relative sprite
		self.rel = rel

### Struts

class translationStrut(relBody, baseBody):
	"""A sprite that applies an offset from a parent sprite onto a child sprite."""
	
	def __init__(self, *args, xoffset = 0, yoffset = 0, **kwargs):
		super().__init__(*args, **kwargs)
		self._xoffset = xoffset
		self._yoffset = yoffset
	
	def update(self, *args):
		super().update(*args)
		self.rect.center = self._strut()
	
	def _strut(self, x = None, y = None, **kwargs):
		x = x or self._xoffset
		y = y or self._yoffset
		rc = self.rel.rect.center
		return (rc[0] + x, rc[1] + y)
	
	@property
	def xoffset(self):
		return self._xoffset
	
	@xoffset.setter
	def xoffset(self, x):
		self._xoffset = x
	
	@property
	def yoffset(self):
		return self._yoffset
	
	@yoffset.setter
	def yoffset(self, y):
		self._yoffset = y

class flipStrut(translationStrut):
	"""A sprite that takes into account its parent's flip state when translating."""
	def _strut(self, x = None, y = None, **kwargs):
		x = x or self._xoffset
		y = y or self._yoffset
		if self.rel.flipx:
			x = -x
		if self.rel.flipy:
			y = -y
		return super()._strut(x = x, y = y, **kwargs)

class rotationStrut(translationStrut):
	"""A sprite that takes into account its parent's rotation when translating."""
	def _strut(self, x = None, y = None, **kwargs):
		x = x or self._xoffset
		y = y or self._yoffset
		theta = - self.rel._theta # Theta is reversed since the y-axis is flipped upside down from normal
		(x, y) = ( # https://en.wikipedia.org/wiki/Rotation_matrix
			x * math.cos(theta) - y * math.sin(theta),
			x * math.sin(theta) + y * math.cos(theta)
		)
		return super()._strut(x = x, y = y, **kwargs)

class fullStrut(flipStrut, rotationStrut):
	"""A sprite that takes into account its parent's flip state and rotation when translating."""
	# We do not reverse the angle when the image is only flipped 1 way in order to make programming easier
	
	pass # '_strut's calls are order as: flipStrut, rotationStrut, and translationStrut, which eliminates our need to implement this manually
