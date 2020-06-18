#!/bin/python3

import pygame as pg

from core.Systems import (
	Draw as Draw,
	Velocity as Velocity,
	RotVel as RotVel,
	Rotation as Rotation,
	FlipDoll as FlipDoll,
	RotDoll as RotDoll,
	Strut as Strut,
)

from core import (
	Events as Events,
	InitQuit as InitQuit,
	G as G,
)

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
	RotVel.update(elapsed)
	
	FlipDoll.update()
	RotDoll.update()
	Strut.update()
	
	Draw.render()
	pg.display.update(Draw.update(G.SCREEN))
	Draw.clear(G.SCREEN, G.BGD)
	
	Rotation.collect()
	
	elapsed = G.CLOCK.tick(60)

def main():
	init()
	
	while True:
		update()

main()
