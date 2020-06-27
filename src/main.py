#!/bin/python3

import pygame as pg

from core import (
	InitQuit,
	Events,
	G,
	Resource as R,
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

scene = bgd = None

def init():
	InitQuit.init()
	
	global scene, bgd
	scene = Level.load("./LEVELS/tutorial.json")
	bgd = scene.copy()
	
	Camera.set(0, 0)
	
	Events.register(pg.QUIT, lambda e: InitQuit.quit())
	
	Draw.borderWidth = 4

elapsed = 0
import itertools
counter = itertools.count()

def update():
	global elapsed
	
	Events.update()
	
	Accel.update(elapsed)
	Velocity.update(elapsed)
	RotVel.update(elapsed)
	
	FlipDoll.update()
	RotDoll.update()
	
	Draw.render()
	
	Position.update()
	Collision.update()
	Strut.update()
	Position.update() # I hate double-updating the positions, but this is the best way that I know of right now to make 'bumping' work smoothly with struts
	
	global scene, bgd
	Draw.update(scene, R.RR[Camera.RectID])
	Camera.update(scene)
	Draw.clear(scene, bgd, R.RR[Camera.RectID])
	
	Rotation.collect()
	
	elapsed = G.CLOCK.tick(60)
	
	global counter
	if next(counter) % 60 == 0:
		print(G.CLOCK.get_fps())

def main():
	init()
	
	while True:
		update()

main()
