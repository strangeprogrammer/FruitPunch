#!/bin/python3

import pygame
# import sys

def main():
	pygame.init()
	# pygame.quit()
	# sys.exit()
	print("killme", file = open("./killme.fifo", mode = "w"))

main()
