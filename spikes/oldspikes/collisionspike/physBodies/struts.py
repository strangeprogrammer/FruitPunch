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
		self.center = self._strut()
	
	def _strut(self, x = None, y = None, **kwargs):
		x = x or self._xoffset
		y = y or self._yoffset
		rc = self.rel.center
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
