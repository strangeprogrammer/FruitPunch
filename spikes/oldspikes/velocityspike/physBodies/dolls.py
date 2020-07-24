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



from .baseBodies import relBody

class flipDoll(flipBody, relBody):
	"""A sprite that flips based upon the flip state of its parent."""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.oldFlips = self.getFlips()
	
	def getFlips(self):
		return (
			bool(self._flipx) ^ bool(self.rel.flipx),
			bool(self._flipy) ^ bool(self.rel.flipy),
		)
	
	def _body(self, **kwargs):
		flipx, flipy = self.getFlips()
		if self.oldFlips != (flipx, flipy):
			self.oldFlips = (flipx, flipy)
			self._dirtyFlip = True
		
		return super()._body(flipx = flipx, flipy = flipy, **kwargs)

class rotationDoll(rotationBody, relBody):
	"""A sprite that rotates based upon the rotation of its parent."""
	
	def _body(self, **kwargs):
		return super()._body(theta = self._theta + self.rel._theta, **kwargs)

class fullDoll(flipDoll, rotationDoll):
	"""A sprite that flips and rotates based upon the flip state and rotation of its parent."""
	
	pass
