#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from System import System

class ContAnimSystem(System): # Continuous Animation System
	def update(self, time):
		for sprite in self.sprites():
			sprite.image = sprite.origImage.copy()
			
			for animation in sprite.contAnimations:
				
				if animation.centerPreserving:
					oldCenter = sprite.rect.center
				
				animation(sprite, time)
				
				if animation.rectGenerating:
					sprite.rect = sprite.image.get_rect()
				
				if animation.centerPreserving:
					sprite.rect.center = oldCenter
