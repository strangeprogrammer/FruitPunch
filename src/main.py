#!/bin/python3

import pygame as pg

import core.Events as Events
import core.Systems.Draw as Draw
import core.Systems.Velocity as Velocity
import core.InitQuit as InitQuit

import core.G as G

def init():
	InitQuit.init()
	
	G.BGD = G.SCREEN.copy()
	pg.display.flip()
	
	Events.register(pg.QUIT, lambda e: InitQuit.quit())

elapsed = 0

def update():
	global elapsed
	
	Events.update()
	Velocity.update(elapsed)
	
	Draw.update(G.SCREEN)
	pg.display.flip()
	Draw.clear(G.SCREEN, G.BGD)
	
	elapsed = G.CLOCK.tick(60)

def main():
	init()
	
	while True:
		update()

main()
