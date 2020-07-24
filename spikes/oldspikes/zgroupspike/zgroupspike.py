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



import pygame

class layerSprite(pygame.sprite.Sprite):
	def __init__(self, *groups, path = None, layer = 0):
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self._layer = layer
		super().__init__(*groups)
	
	def setImage(self, image):
		self.image = image
	
	def getImage(self):
		return self.image
	
	def setRect(self, rect):
		self.rect = rect
	
	def getRect(self):
		return self.rect
	
	def setLayer(self, layer):
		self._layer = layer
	
	def getLayer(self):
		return self._layer
	
	def __hash__(self):
		return id(self)

def populate():
	allSprites = pygame.sprite.LayeredUpdates()
	
	red	= layerSprite(allSprites, path = "./RedSquare.png", layer = -2)
	blue	= layerSprite(allSprites, path = "./BlueSquare.png", layer = -1)
	grey	= layerSprite(allSprites, path = "./GreyRectangle.png", layer = 0)
	green	= layerSprite(allSprites, path = "./GreenSquare.png", layer = 1)
	yellow	= layerSprite(allSprites, path = "./YellowSquare.png", layer = 2)
	
	grey.setRect(grey.getRect().move(200, 200))
	red.getRect().center = grey.getRect().topleft
	blue.getRect().center = grey.getRect().bottomleft
	green.getRect().center = grey.getRect().topright
	yellow.getRect().center = grey.getRect().bottomright
	
	return allSprites

def main():
	pygame.init()
	
	allSprites = populate()
	screen = pygame.display.set_mode()
	
	screen.fill((255, 255, 255))
	allSprites.draw(screen)
	pygame.display.flip()
	
	goflag = True
	while goflag:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				goflag = False
				break
	
	pygame.quit()

main()
