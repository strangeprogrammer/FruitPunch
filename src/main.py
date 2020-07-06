#!/bin/python3

import pygame as pg
import sqlalchemy as sqa

from core import (
	InitQuit,
	Events,
	G,
	Component as C,
	Resource as R,
	Level,
	Time,
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

bgd = None

def init():
	InitQuit.init()
	
	global bgd
	bgd = Level.load("./LEVELS/tutorial.json")
	
	Camera.bind(
		G.CONN.execute(
			sqa	.select([
					C.PLYC.c.EntID,
				]).select_from(
					C.PLYC,
				)
		).fetchall()[0][0]
	)
	
	Camera.update()
	
	Events.register(pg.QUIT, lambda e: InitQuit.quit())

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
	
	global bgd
	Draw.update(bgd, R.RR[Camera.RectID])
	
	Rotation.collect()
	
	Time.update()
	
	global counter
	if next(counter) % 60 == 0:
		print(Time._clock.get_fps())

def main():
	init()
	
	while True:
		update()

main()
