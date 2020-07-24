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
player1 = None
player2 = None
togglers = []
manager = []
drawables = None
velStep = 0.05

def handleQuit(e):
	pg.quit()
	exit(0)

def goUp( player):
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

from makeBodies import makeBodies
from collMan import collMan

def init():
	global handlers, keyDownHandlers, clock, screen, bgd, player1, player2, togglers, manager, drawables
	
	handlers[pg.QUIT] = handleQuit
	handlers[pg.KEYDOWN] = handleKeyDown
	
	keyDownHandlers[pg.K_UP]	= lambda e: goUp(player1)
	keyDownHandlers[pg.K_DOWN]	= lambda e: goDown(player1)
	keyDownHandlers[pg.K_LEFT]	= lambda e: goLeft(player1)
	keyDownHandlers[pg.K_RIGHT]	= lambda e: goRight(player1)
	
	keyDownHandlers[pg.K_w]		= lambda e: goUp(player2)
	keyDownHandlers[pg.K_s]		= lambda e: goDown(player2)
	keyDownHandlers[pg.K_a]		= lambda e: goLeft(player2)
	keyDownHandlers[pg.K_d]		= lambda e: goRight(player2)
	
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	pg.display.flip()
	
	bgd = screen.copy()
	
	clock = pg.time.Clock()
	
	(player1, player2, togglers) = makeBodies(clock)
	manager = collMan(togglers, pg.sprite.Group(player1, player2))
	
	drawables = pg.sprite.LayeredUpdates(player1, player2, *togglers)

def update():
	global clock, screen, bgd, player1, player2, togglers, manager, drawables
	
	clock.tick(60)
	
	doEvents()
	
	player1.update(clock.get_time())
	player2.update(clock.get_time())
	for t in togglers:
		t.update()
	
	manager.update()
	
	pg.display.update(drawables.draw(screen))
	
	drawables.clear(screen, bgd)

def main():
	init()
	
	while True:
		update()

main()
