#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from .baseBodies import baseBody

class velocityBody(baseBody):
	def __init__(self, *args, velocity = [0, 0], clock = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.velocity = list(velocity) # Just in case a tuple is passed in on accident
		self.clock = clock
	
	def update(self, *args):
		self._mobilize()
		super().update(*args)
	
	def _mobilize(self, clock = None):
		clock = clock or self.clock
		if clock is None:
			dt = 0
		else:
			dt = clock.get_time()
		
		self.center[0] += self.velocity[0] * dt
		self.center[1] += self.velocity[1] * dt
	
	def stop(self):
		self.velocity = [0, 0]
