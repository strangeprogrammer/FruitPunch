#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

import G
import makeTables
import makeResources
import makeEntities

def DBInit():
	G.ENGINE = sqa.create_engine("sqlite:///")
	G.DB = sqa.MetaData()
	G.CONN = G.ENGINE.connect()

def DisplayInit():
	G.SCREEN = pg.display.set_mode()
	G.SCREEN.fill( (255, 255, 255) )

def init():
	DBInit()
	DisplayInit()
	makeTables.makeTables()
	makeResources.makeResources()
	makeEntities.makeEntities()

def quit():
	pg.quit()
	
	import sys
	sys.exit(0)
