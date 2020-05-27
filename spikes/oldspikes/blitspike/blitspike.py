#!/bin/python3

# Draws a big square on the screen, but only draws half of a small square across the big square's right side

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
	
	bigSquare.blit(*square.getall())
	
	screen.fill((255, 255, 255))
	screen.blit(*bigSquare.getall())
	pygame.display.flip()
	
	noexit = True
	while noexit:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				noexit = False
	
	pygame.quit()

main()
