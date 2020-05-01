#!/bin/python3

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
