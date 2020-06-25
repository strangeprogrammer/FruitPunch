#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import json
import math
import pygame as pg

from . import CollHandLib as CHL
from . import Entity

from .Systems import (
	Velocity,
	Accel,
	Rotation,
	RotVel,
	Collision,
)

def load(fileName):
	with open(fileName) as fp:
		level = json.load(fp)
		
		_makePlayer(**level["player"])
		
		for ceiling in level["ceilings"]:
			_makeCeiling(**ceiling)
		
		for floor in level["floors"]:
			_makeFloor(**floor)
		
		for leftWall in level["leftWalls"]:
			_makeLeftWall(**leftWall)
		
		for rightWall in level["rightWalls"]:
			_makeRightWall(**rightWall)

def _loadimage(fileName):
	return pg.image.load(fileName).convert_alpha()

def _makePlayer(image, x, y):
	img = _loadimage(image)
	rect = img.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(img, rect, (x, y))
	
	Velocity.register(EntID)
	Accel.register(EntID)
	Accel.set(EntID, 0, 0.4 / 1000)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	Collision.register(EntID)
	
	return EntID

def _makeBumping(ejectHandlerID, image, x, y):
	img = _loadimage(image)
	rect = img.get_rect()
	
	EntID, ImageID, RectID = Entity.create(img, rect, (x, y))
	
	Collision.register(EntID)
	Collision.setState(EntID, ejectHandlerID, ejectHandlerID, 0)

_makeCeiling	= lambda image, x, y: _makeBumping(CHL.ejectDownID, image, x, y)
_makeFloor	= lambda image, x, y: _makeBumping(CHL.ejectUpID, image, x, y)
_makeLeftWall	= lambda image, x, y: _makeBumping(CHL.ejectRightID, image, x, y)
_makeRightWall	= lambda image, x, y: _makeBumping(CHL.ejectLeftID, image, x, y)