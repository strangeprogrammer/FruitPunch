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
import math

from bodyparts import basicBody

def makeBodies():
	x = basicBody((500, 500))
	y = basicBody((700, 300))
	return [x, y]

def updateBodies(bodies, *args):
	for group in bodies:
		group.update(*args)

def drawBodies(bodies, surface):
	rects = []
	for group in bodies:
		rects += group.draw(surface)
	return rects

def clearBodies(bodies, surface, bgd):
	for group in bodies:
		group.clear(surface, bgd)

def main():
	pygame.init()
	
	screen = pygame.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	pygame.display.flip()
	bodies = makeBodies()
	
	goflag = True
	while goflag:
		updateBodies(bodies, pygame.time.get_ticks())
		pygame.display.update(drawBodies(bodies, screen))
		clearBodies(bodies, screen, bgd)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				goflag = False
				break
	
	pygame.quit()

main()
