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

from core.Misc import LevelLoadException

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

goflag = True

def quit(*args, **kwargs):
	global goflag
	goflag = False

def main():
	pg.init()
	Events.register(pg.QUIT, quit)
	
	Level.load("./LEVELS/tutorial.json")
	
	global goflag
	while goflag:
		try:
			update()
		except LevelLoadException as e:
			Level.unload()
			Level.load(e.filename)
	
	Level.unload()
	pg.quit()
	sys.exit(0)

main()
