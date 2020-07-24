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



import pygame as pg

class entity(pg.sprite.Sprite):
	def __init__(
		self,
		*groups,
		corpus = {},
		animations = {"idle": lambda corpus, moment, duration: None},
		actions = {"idle": lambda entity, **worldState: None},
		brain = lambda entity, **worldState: [],
		init = lambda entity: None,
		**kwargs,
	):
		super().__init__(*groups)
		self.corpus = corpus
		self.animGroup = pg.sprite.LayeredUpdates(corpus.values())
		self.animations = animations
		self.activeAnims = {}
		self.culledAnims = set(self.animations.keys())
		self.actions = actions
		self.brain = brain
		self.state = {} # KVP's used by 'brain'
		init(self)
	
	def draw(self, surface):
		return self.animGroup.draw(surface)
	
	def clear(self, surface, bgd):
		return self.animGroup.clear(surface, bgd)
	
	def _doActions(self, **worldState):
		for actionName in self.brain(self, culledAnims = self.culledAnims, **worldState):
			self.actions[actionName](self, **worldState)
	
	def _doAnims(self, worldTime):
		for animName, (startTime, duration) in self.activeAnims.items():
			self.animations[animName](self.corpus, worldTime - startTime, duration)
	
	def startAnim(self, animName, worldTime, duration):
		self.activeAnims[animName] = (worldTime, duration)
	
	def stopAnim(self, animName):
		del self.activeAnims[animName]
		self.culledAnims.add(animName)
	
	def _cullAnims(self, worldTime):
		for animName, (startTime, duration) in self.activeAnims.copy().items():
			if startTime + duration < worldTime:
				self.stopAnim(animName)
	
	def update(self, worldTime, **worldState):
		self._cullAnims(worldTime)
		self._doActions(worldTime = worldTime, **worldState)
		self._doAnims(worldTime)
		self.culledAnims.clear()
		self.animGroup.update(*worldState.get("animArgs", []), **worldState.get("animKwrgs", {}))
