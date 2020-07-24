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



# Draws a big square on the screen as well as a small square across the big square's right side

import pygame

class entity():
	def __init__(self, path):
		self.screen = pygame.image.load(path)
		self.rect = self.screen.get_rect()
	
	def move(self, *args):
		self.rect = self.rect.move(*args)
	
	def blit(self, *args):
		self.screen.blit(*args)
	
	def getall(self):
		return (self.screen, self.rect)

def main():
	pygame.init()
	
	screen = pygame.display.set_mode()
	
	square = entity("./Square.png")
	bigSquare = entity("./BigSquare.png")
	
	square.move(224, 96)
	bigSquare.move(250, 250)
	
	screen.fill((255, 255, 255))
	screen.blit(square.screen, square.rect.move(*bigSquare.rect.topleft))
	screen.blit(*bigSquare.getall())
	pygame.display.flip()
	
	noexit = True
	while noexit:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				noexit = False
	
	pygame.quit()

main()
