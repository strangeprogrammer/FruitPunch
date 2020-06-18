#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
from sys import exit

from . import G
from . import Component
from . import Tables
from . import makeResources

from . import Entity
from .Systems import Draw
from .Systems import Flip
from .Systems import Rotation
from .Systems import Velocity
from .Systems import RotVel
from .Systems import FlipDoll
from .Systems import RotDoll
from .Systems import Strut

from . import PlayerMove

from . import makeEntities

def init():
	pg.init()
	
	Component.DBInit()
	Tables.init()
	makeResources.makeResources()
	
	Entity.init()
	Draw.init()
	Flip.init()
	Rotation.init()
	Velocity.init()
	RotVel.init()
	FlipDoll.init()
	RotDoll.init()
	Strut.init()
	
	Draw.addRenderStep(Flip.render)
	Draw.addRenderStep(Rotation.render)
	
	PlayerMove.init()
	
	makeEntities.makeEntities()
	
	G.CLOCK = pg.time.Clock()

def quit():
	pg.quit()
	
	exit(0)
