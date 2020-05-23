#!/bin/python3

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
