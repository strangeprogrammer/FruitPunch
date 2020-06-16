#!/bin/python3

import pygame as pg

import core.Events as Events
import core.Systems.Draw as Draw
import core.Systems.Velocity as Velocity
import core.Systems.RotVel as RotVel
import core.Systems.Rotation as Rotation
import core.Systems.FlipDoll as FlipDoll
import core.Systems.RotDoll as RotDoll
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
	RotVel.update(elapsed)
	
	FlipDoll.update()
	RotDoll.update()
	
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
