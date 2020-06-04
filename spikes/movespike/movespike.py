#!/bin/python3

import pygame as pg

import Events
import DrawSystem
import PlayerMoveSystem
import InitQuit

import G

def init():
	InitQuit.init()
	
	G.BGD = G.SCREEN.copy()
	pg.display.flip()
	
	Events.register(pg.QUIT, lambda e: InitQuit.quit())

def update():
	Events.update()
	PlayerMoveSystem.update()
	
	DrawSystem.update(G.SCREEN)
	pg.display.flip()
	DrawSystem.clear(G.SCREEN, G.BGD)
	
	G.CLOCK.tick(60)

def main():
	init()
	
	while True:
		update()

main()
