#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

import G
import makeTables
import makeResources
import makeEntities
import DrawSystem
import PlayerMoveSystem

def DBInit():
	G.ENGINE = sqa.create_engine("sqlite:///")
	G.DB = sqa.MetaData()
	G.CONN = G.ENGINE.connect()

def init():
	pg.init()
	
	DBInit()
	makeTables.makeTables()
	makeResources.makeResources()
	makeEntities.makeEntities()
	
	DrawSystem.init()
	PlayerMoveSystem.init()
	
	G.CLOCK = pg.time.Clock()

def quit():
	pg.quit()
	
	import sys
	sys.exit(0)
