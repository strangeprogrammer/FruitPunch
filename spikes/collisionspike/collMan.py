#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

class collMan():
	"""Object to send collision events to Sprites in Group 1
	when they collide with Sprites in Group 2."""
	def __init__(self, g1, g2, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.g1 = g1
		self.g2 = g2
		self.prevCollisions = set()
	
	def _getCollisions(self):
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
