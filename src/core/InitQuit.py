#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
from sys import exit

from . import (
	G,
	Component,
	Resource,
	Time,
	PlayerMove,
	CollHandLib,
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

def init():
	pg.init()
	
	Component.init()
	Resource.init()
	
	Draw.init()
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
	
	Draw.addRenderStep(Flip.render)
	Draw.addRenderStep(Rotation.render)
	
	Camera.init()
	
	PlayerMove.init()
	
	CollHandLib.init()
	
	Time.init()

def quit():
	CollHandLib.quit()
	
	Component.quit()
	
	pg.quit()
	
	exit(0)
