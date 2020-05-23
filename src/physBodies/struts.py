#!/bin/python3

import math

from .baseBodies import relBody

class translationStrut(relBody):
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
			x * math.sin(theta) + y * math.cos(theta),
		)
		return super()._strut(x = x, y = y, **kwargs)

class fullStrut(flipStrut, rotationStrut):
	"""A sprite that takes into account its parent's flip state and rotation when translating."""
	# We do not reverse the angle when the image is only flipped 1 way in order to make programming easier
	
	pass # '_strut's calls are order as: flipStrut, rotationStrut, and translationStrut, which eliminates our need to implement this manually
