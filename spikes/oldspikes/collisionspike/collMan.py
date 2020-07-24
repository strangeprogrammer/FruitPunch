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



class collMan():
	"""Object to send collision events to Sprites in Group 1
	when they collide with Sprites in Group 2."""
	def __init__(self, g1, g2, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.g1 = g1
		self.g2 = g2
		self.prevCollisions = set()
	
	def _getCollisions(self): # TODO: Improve this to use a better method
		self.collisions = set()
		
		import itertools
		for host, collider in itertools.product(self.g1.sprites(), self.g2.sprites()):
			if host.rect.colliderect(collider.rect):
				self.collisions |= {(host, collider)}
	
	def _getEvents(self):
		staleCollisions = self.prevCollisions - self.collisions
		newCollisions = self.collisions - self.prevCollisions
		
		self.prevCollisions = self.collisions
		
		return (staleCollisions, newCollisions)
	
	def _doOnCollide(self, newCollisions):
		for host, collider in newCollisions:
			host.onCollide(collider)
	
	def _doOffCollide(self, staleCollisions):
		for host, collider in staleCollisions:
			host.offCollide(collider)
	
	def update(self):
		self._getCollisions()
		(staleCollisions, newCollisions) = self._getEvents()
		self._doOffCollide(staleCollisions)
		self._doOnCollide(newCollisions)
