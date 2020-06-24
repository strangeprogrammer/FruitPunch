#!/bin/python3

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
	screen.blit(*bigSquare.getall())
	pygame.display.flip()
	
	noexit = True
	while noexit:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				noexit = False
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_UP:
					square.move(0, -1)
				elif e.key == pygame.K_DOWN:
					square.move(0, 1)
				elif e.key == pygame.K_LEFT:
					square.move(-1, 0)
				elif e.key == pygame.K_RIGHT:
					square.move(1, 0)
				elif e.key == pygame.K_SPACE:
					square.rect.topleft = pygame.mouse.get_pos()
		
		screen.fill((255, 255, 255))
		screen.blit(*square.getall(), pygame.Rect(0, 0, int(square.rect.width / 2), square.rect.height))
		screen.blit(*bigSquare.getall())
		pygame.display.flip()
	
	pygame.quit()

main()
