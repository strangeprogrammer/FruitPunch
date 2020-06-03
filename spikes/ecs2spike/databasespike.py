#!/bin/python3

import pygame as pg

import Events
import Drawing
import InitQuit

import G

bgd = None

def init():
	InitQuit.init()
	
	global bgd
	bgd = G.SCREEN.copy()
	pg.display.flip()
	
	Events.register(pg.QUIT, lambda e: InitQuit.quit())

def update():
	Events.update()
	
	global bgd
	Drawing.update(G.SCREEN)
	pg.display.flip()
	Drawing.clear(G.SCREEN, bgd)

def main():
	init()
	
	while True:
		update()

main()
