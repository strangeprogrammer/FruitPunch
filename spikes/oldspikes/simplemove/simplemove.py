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

white = (255, 255, 255)

def keyState(events):
	retval = {}
	for e in events:
		if e.type == pygame.KEYDOWN:
			retval[pygame.key.name(e.key)] = True
		elif e.type == pygame.KEYUP:
			retval[pygame.key.name(e.key)] = False
	return retval

def movement(buttons):
	retval = (0, 0)
	
	if buttons.get('up', None) == True:
		retval = (0, -5)
	elif buttons.get('up', None) == False:
		retval = (0, 5)
	
	if buttons.get('down', None) == True:
		retval = (0, 5)
	elif buttons.get('down', None) == False:
		retval = (0, -5)
	
	if buttons.get('left', None) == True:
		retval = (-5, 0)
	elif buttons.get('left', None) == False:
		retval = (5, 0)
	
	if buttons.get('right', None) == True:
		retval = (5, 0)
	elif buttons.get('right', None) == False:
		retval = (-5, 0)
	
	return retval

def getKillSig(events):
	for e in events:
		if e.type == pygame.QUIT:
			return False
	return True

def progLoop(screen, square, squarebox):
	squareVelocity = [0, 0]
	
	events = pygame.event.get()
	while getKillSig(events):
		buttons = keyState(events)
		
		m = movement(buttons)
		
		squareVelocity[0] += m[0]
		squareVelocity[1] += m[1]
		squarebox = squarebox.move(*squareVelocity)
		
		screen.fill(white)
		screen.blit(square, squarebox)
		pygame.display.flip()
		
		events = pygame.event.get()

import sys

def main():
	pygame.init()
	
	screen = pygame.display.set_mode()
	
	square = pygame.image.load("Square.png")
	squarebox = square.get_rect()
	
	progLoop(screen, square, squarebox)
	
	print("Kill me now")

main()
