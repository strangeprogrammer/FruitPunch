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



from pygame import sprite as pgs

from ConflictMonitor import SymmetricConflictMonitor as BCM

class Corpus(pgs.Sprite):
	def __init__(self, *groups, corpus = {}, **kwargs):
		super().__init__(*groups)
		self.corpus = corpus
		self.animGroup = pgs.LayeredUpdates(corpus.values())
	
	def draw(self, surface):
		return self.animGroup.draw(surface)
	
	def clear(self, surface, bgd):
		return self.animGroup.clear(surface, bgd)
	
	def update(self, **worldState):
		self.animGroup.update(*worldState.get("animArgs", []), **worldState.get("animKwrgs", {}))

class AnimationMonitor(Corpus):
	def __init__(
		self,
		*args,
		scm = None,
		animations = {"idle": lambda corpus, moment, duration: None},
		**kwargs,
	):
		super().__init__(*args, **kwargs)
		if scm is None:
			scm = SCM()
			for animName in animations:
				scm.addConflicts(animName, {animName}) # Default to having every animation conflict with itself
		self.scm = scm
		self.animations = animations
		self.activeAnims = {}
		self.culledAnims = set(self.animations.keys())
	
	def update(self, worldTime, **worldState):
		for animName, (startTime, duration) in self.activeAnims.items():
			self.animations[animName](self.corpus, worldTime - startTime, duration)
		super().update(**worldState)
	
	def cullAnims(self, worldTime):
		for animName, (startTime, duration) in self.activeAnims.copy().items():
			if startTime + duration < worldTime:
				self.stopAnim(animName)
	
	def startAnim(self, animName, worldTime, duration):
		if animName in self.animations: # Is this a valid animation?
			predicate = lambda activeAnim: self.scm.hasConflict(animName, activeAnim)
			if not any(map(predicate, self.activeAnims)): # Does this animation conflict with any currently running?
				self.activeAnims[animName] = (worldTime, duration)
				return True
		return False
	
	def stopAnim(self, animName):
		if animName in self.activeAnims:
			del self.activeAnims[animName]
			self.culledAnims.add(animName)
			return True
		return False

class Entity(AnimationMonitor):
	def __init__(
		self,
		*args,
		brain = lambda ent, **worldState: None,
		**kwargs
	):
		super().__init__(*args, **kwargs)
		self.brain = brain
	
	def update(self, worldTime, **worldState):
		self.cullAnims(worldTime)
		self.brain(self, worldTime = worldTime, **worldState)
		self.culledAnims.clear()
		super().update(worldTime, **worldState)
