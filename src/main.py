#!/bin/python3

import pygame as pg

from core import (
	InitQuit,
	Events,
	G,
)

from core.Systems import (
	Draw,
	Position,
	Rotation,
	Velocity,
	RotVel,
	FlipDoll,
	RotDoll,
	Strut,
	Collision,
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
	
	Position.update()
	Collision.update()
	
	pg.display.update(Draw.update(G.SCREEN))
	Draw.clear(G.SCREEN, G.BGD)
	
	Rotation.collect()
	
	elapsed = G.CLOCK.tick(60)

def main():
	init()
	
	while True:
		update()

main()
