#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from physBodies.baseBodies import baseBody

class velocityBody(baseBody):
	def __init__(self, *args, velocity = [0, 0], **kwargs):
		super().__init__(*args, **kwargs)
		self.velocity = velocity
	
	def update(self, dt, *args):
		self._mobilize(dt)
		super().update(*args)
	
	def _mobilize(self, dt):
		self.center[0] += self.velocity[0] * dt
		self.center[1] += self.velocity[1] * dt
