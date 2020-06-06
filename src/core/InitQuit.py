#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from . import G
from . import Backend
from . import makeTables
from . import makeResources

from . import Entity
from .Systems import Draw
from .Systems import Velocity

from . import PlayerMove

from . import makeEntities

def init():
	pg.init()
	
	Backend.DBInit()
	makeTables.makeTables()
	makeResources.makeResources()
	
	Entity.init()
	Draw.init()
	Velocity.init()
	
	PlayerMove.init()
	
	makeEntities.makeEntities()
	
	G.CLOCK = pg.time.Clock()

def quit():
	pg.quit()
	
	import sys
	sys.exit(0)
