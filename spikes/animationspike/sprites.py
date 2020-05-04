#!/bin/python3

import pygame

from abc import ABC, abstractmethod

class drawnSprite(ABC):
	@abstractmethod
	def draw(self, surface):
		pass
