#!/bin/python3

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
