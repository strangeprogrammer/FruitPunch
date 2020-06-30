#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import json
import math
import pygame as pg

from . import CollHandLib as CHL
from . import Entity
from .Misc import Rect

from .Systems import (
	Velocity,
	Accel,
	Rotation,
	RotVel,
	Collision,
)

def _loadImage(fileName):
	return pg.image.load(fileName).convert_alpha()

def load(fileName):
	with open(fileName) as fp:
		level = json.load(fp)
		
		_makePlayer(**level["player"])
		
		for wall in level.get("walls", []):
			_makeEject(**wall)
		
		return _loadImage(level["background"])

def _makePlayer(image, x, y):
	img = _loadImage(image)
	rect = Rect(img.get_rect())
	
	EntID, ImageID, RectID = Entity.createPlayer(img, rect, (x, y))
	
	Velocity.register(EntID)
	Accel.register(EntID)
	Accel.store(EntID, 0, 0.8 / 1000)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	Collision.register(EntID)
	
	return EntID

def _makeEject(image, x, y):
	img = _loadImage(image)
	rect = Rect(img.get_rect())
	
	EntID, ImageID, RectID = Entity.create(img, rect, (x, y))
	
	Collision.register(EntID)
	Collision.store(EntID, CHL.ejectID, CHL.ejectID, 0)
