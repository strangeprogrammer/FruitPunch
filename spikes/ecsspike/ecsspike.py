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

eventHandles = {}
systems = {}
allSprites = None
clock = pg.time.Clock()
screen = None
bgd = None

def cleanQuit():
	pg.quit()
	import sys
	sys.exit(0)

def processEvents():
	global eventHandles
	for e in pg.event.get():
		eventHandles.get(e.type, lambda: None)()

def mainLoop():
	processEvents()
	
	time = pg.time.get_ticks()
	
	global systems
	systems["ContAnimSystem"].update(time)
	
	global screen, bgd
	pg.display.update(systems["DrawSystem"].draw(screen))
	systems["DrawSystem"].clear(screen, bgd)
	
	global clock
	clock.tick(60)

def makeAll():
	global allSprites
	from makeSprites import makeSprites
	allSprites = makeSprites()
	
	global systems
	from DrawSystem import DrawSystem
	systems["DrawSystem"] = DrawSystem(allSprites.sprites())
	
	from ContAnimSystem import ContAnimSystem
	systems["ContAnimSystem"] = ContAnimSystem(allSprites.sprites())

def main():
	global screen, bgd
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	
	pg.display.flip()
	
	global eventHandles
	eventHandles[pg.QUIT] = cleanQuit
	
	makeAll()
	
	while True:
		mainLoop()

main()
