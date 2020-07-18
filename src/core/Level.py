#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from . import (
	G,
	Component,
	Component as C,
	Resource,
	Time,
	PlayerMove,
	CollHandLib,
	LevelLoader,
)

from .Systems import (
	Camera,
	Draw,
	Flip,
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

def load(fileName):
	Component.init()
	Resource.init()
	
	Flip.init()
	
	Position.init()
	Rotation.init()
	Velocity.init()
	RotVel.init()
	Accel.init()
	
	FlipDoll.init()
	RotDoll.init()
	Strut.init()
	
	Collision.init()
	
	Camera.init()
	
	Draw.init()
	Draw.addRenderStep(Flip.render)
	Draw.addRenderStep(Rotation.render)
	
	PlayerMove.init()
	
	CollHandLib.init()
	
	Time.init()
	
	
	
	Draw.bgd = LevelLoader.load(fileName)
	
	Camera.bind(
		G.CONN.execute(
			C.PLYC.select()
		).scalar()
	)
	
	Camera.update()

def unload():
	CollHandLib.quit()
	
	PlayerMove.quit()
	
	Draw.quit()
	
	Camera.quit()
	
	Collision.quit()
	
	Strut.quit()
	RotDoll.quit()
	FlipDoll.quit()
	
	Accel.quit()
	RotVel.quit()
	Velocity.quit()
	Rotation.quit()
	Position.quit()
	
	Flip.quit()
	
	Resource.quit()
	
	Component.quit()
