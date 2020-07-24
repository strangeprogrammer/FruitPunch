#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

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
