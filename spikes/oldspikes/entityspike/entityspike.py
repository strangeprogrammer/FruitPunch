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
from pygame.sprite import LayeredUpdates as LU

from newPlayer import newPlayer

keyDHandles = {}
keyUHandles = {}
playerActions = []

def quitProg():
	pg.quit()
	quit()

def keyDown(key):
	global keyDHandles
	keyDHandles.get(key, lambda: None)()

def keyUp(key):
	global keyUHandles
	keyUHandles.get(key, lambda: None)()

def handleEvent(e):
	if e.type == pg.QUIT:
		quitProg()
	elif e.type == pg.KEYDOWN:
		keyDown(e.key)
	elif e.type == pg.KEYUP:
		keyUp(e.key)

def init():
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	pg.display.flip()
	
	player = newPlayer()
	
	global keyUHandles
	global keyDHandles
	global playerActions
	keyDHandles[pg.K_a] = lambda: playerActions.append("RDown")
	keyUHandles[pg.K_a] = lambda: playerActions.append("RUp")
	keyDHandles[pg.K_s] = lambda: playerActions.append("BDown")
	keyUHandles[pg.K_s] = lambda: playerActions.append("BUp")
	keyDHandles[pg.K_d] = lambda: playerActions.append("GDown")
	keyUHandles[pg.K_d] = lambda: playerActions.append("GUp")
	keyDHandles[pg.K_f] = lambda: playerActions.append("YDown")
	keyUHandles[pg.K_f] = lambda: playerActions.append("YUp")
	
	return (screen, player, screen.copy())

def progBody(screen, player, bgd):
	list(map(handleEvent, pg.event.get())) # Must be forced out of laziness with 'list'
	
	global playerActions
	player.update(actions = playerActions, worldTime = pg.time.get_ticks())
	
	pg.display.update(player.draw(screen))
	player.clear(screen, bgd)
	
	playerActions.clear()

def main():
	pg.init()
	
	state = init()
	while True:
		progBody(*state)

main()
