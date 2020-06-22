#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
from sys import exit

from . import G
from . import Database
from . import Component
from . import Resource

from . import Entity
from .Systems import (
	Draw,
	Flip,
	Position,
	Rotation,
	Velocity,
	RotVel,
	FlipDoll,
	RotDoll,
	Strut,
	Collision,
)

from . import PlayerMove
from . import makeEntities

def init():
	pg.init()
	
	Database.init()
	Component.init()
	Resource.init()
	
	Entity.init()
	Draw.init()
	Flip.init()
	Position.init()
	Rotation.init()
	Velocity.init()
	RotVel.init()
	FlipDoll.init()
	RotDoll.init()
	Strut.init()
	Collision.init()
	
	Draw.addRenderStep(Flip.render)
	Draw.addRenderStep(Rotation.render)
	
	PlayerMove.init()
	
	makeEntities.makeEntities()
	
	G.CLOCK = pg.time.Clock()

def quit():
	pg.quit()
	
	exit(0)
