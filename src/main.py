#!/bin/python3

import pygame as pg
import sqlalchemy as sqa
import sys

from core import (
	Events,
	G,
	Component as C,
	Resource as R,
	LevelLoader,
	Time,
	Level,
)

from core.Systems import (
	Camera,
	Draw,
	Position,
	Rotation,
	Velocity,
	RotVel,
	Accel,
	FlipDoll,
	RotDoll,
	Strut,
	Collision,
)

import itertools
counter = itertools.count()

def update():
	Events.update()
	
	Accel.update()
	Velocity.update()
	RotVel.update()
	
	FlipDoll.update()
	RotDoll.update()
	
	Draw.render()
	
	Position.update()
	
	Collision.update()
	
	Strut.update()
	Position.update() # I hate double-updating the positions, but this is the best way that I know of right now to make 'bumping' work smoothly with struts
	
	Camera.update()
	
	Draw.update()
	
	Rotation.collect()
	
	Time.update()
	
	global counter
	if next(counter) % 60 == 0:
		print(Time._clock.get_fps())

phasenum = 0

def advance(*args, **kwargs):
	global phasenum
	phasenum += 1

def main():
	pg.init()
	Events.register(pg.QUIT, advance)
	
	global phasenum
	
	
	Level.load("./LEVELS/tutorial.json")
	
	while phasenum == 0:
		update()
	
	
	
#	Level.unload()
#	Level.load("./LEVELS/notTutorial.json")
#	
#	while phasenum == 1:
#		update()
	
	Level.unload()
	pg.quit()
	sys.exit(0)

main()
