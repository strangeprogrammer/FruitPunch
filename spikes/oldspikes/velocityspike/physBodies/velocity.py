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
