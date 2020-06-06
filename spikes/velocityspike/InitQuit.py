#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

import G
import Backend
import makeTables
import makeResources

import Entity
import DrawSystem
import VelocitySystem

import PlayerMove

import makeEntities

def init():
	pg.init()
	
	Backend.DBInit()
	makeTables.makeTables()
	makeResources.makeResources()
	
	Entity.init()
	DrawSystem.init()
	VelocitySystem.init()
	
	PlayerMove.init()
	
	makeEntities.makeEntities()
	
	G.CLOCK = pg.time.Clock()

def quit():
	pg.quit()
	
	import sys
	sys.exit(0)
