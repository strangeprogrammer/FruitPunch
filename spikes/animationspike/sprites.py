#!/bin/python3

import pygame

from abc import ABC, abstractmethod

class drawnSprite(ABC):
	@abstractmethod
	def draw(self, surface):
		pass

class layerSprite(pygame.sprite.Sprite):
	def __init__(self, image, rect, *groups, layer = 0, **kwargs):
		self.image = image
		self.rect = rect
		self._layer = layer
		super().__init__(*groups, **kwargs)
	
	def initPath(path, *args, **kwargs):
		image = pygame.image.load(path)
		return __class__(image, image.get_rect(), *args, **kwargs)
	
	def set_image(self, image):
		self.image = image
	
	def get_image(self):
		return self.image
	
	def set_rect(self, rect):
		self.rect = rect
	
	def get_rect(self):
		return self.rect
	
	def set_layer(self, layer):
		self._layer = layer
	
	def get_layer(self):
		return self._layer
	
	def copy(self, *args, **kwargs):
		return self.__class__(self.image.copy(), self.rect.copy(), self.groups(), *args, layer = self._layer, **kwargs)
	
	def __hash__(self):
		return id(self)
