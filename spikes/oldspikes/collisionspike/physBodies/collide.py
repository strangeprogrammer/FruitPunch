#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from .baseBodies import baseBody
from abc import ABC, abstractmethod

class collideBody(baseBody, ABC):
	@abstractmethod
	def onCollide(self, other):
		pass
	
	@abstractmethod
	def offCollide(self, other):
		pass
