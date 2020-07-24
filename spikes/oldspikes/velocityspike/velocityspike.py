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
from sys import exit

handlers = {}
keyDownHandlers = {}
clock = None
screen = None
bgd = None
player = None
drawables = None
velStep = 0.05

def handleQuit(e):
	pg.quit()
	exit(0)

def goUp(player):
	global velStep
	player.velocity[1] -= velStep

def goDown(player):
	global velStep
	player.velocity[1] += velStep

def goLeft(player):
	global velStep
	player.velocity[0] -= velStep

def goRight(player):
	global velStep
	player.velocity[0] += velStep

def handleKeyDown(e):
	global keyDownHandlers
	handle = keyDownHandlers.get(e.key, lambda x: None)
	handle(e)

def doEvents():
	for e in pg.event.get():
		global handlers
		handle = handlers.get(e.type, lambda x: None)
		handle(e)

from makePlayer import makePlayer

def init():
	global handlers, keyDownHandlers, clock, screen, bgd, player, drawables
	
	handlers[pg.QUIT] = handleQuit
	handlers[pg.KEYDOWN] = handleKeyDown
	
	keyDownHandlers[pg.K_UP]	= lambda e: goUp(player)
	keyDownHandlers[pg.K_DOWN]	= lambda e: goDown(player)
	keyDownHandlers[pg.K_LEFT]	= lambda e: goLeft(player)
	keyDownHandlers[pg.K_RIGHT]	= lambda e: goRight(player)
	
	clock = pg.time.Clock()
	
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	
	bgd = screen.copy()
	
	player = makePlayer()
	
	drawables = pg.sprite.LayeredUpdates(player)

def update():
	global clock, screen, bgd, player, drawables
	
	clock.tick(60)
	
	doEvents()
	
	player.update(clock.get_time())
	
	drawables.draw(screen)
	
	# pg.display.update(<BOXES>)
	pg.display.flip()
	
	drawables.clear(screen, bgd)

def main():
	init()
	
	while True:
		update()

main()
