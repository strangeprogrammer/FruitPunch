#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import json
import math
import pygame as pg

from . import CollHandLib as CHL
from . import Entity
from .Misc import Rect
from . import Component as C
from . import Resource as R

from .Systems import (
	Velocity,
	Accel,
	Rotation,
	RotVel,
	Collision,
)

imagedict = {}

def _loadImage(fileName):
	return pg.image.load(
		fileName
	).convert_alpha()

def _makeImages(images):
	return dict(
		map(
			lambda t: [t[0], _loadImage(t[1])],
			images.items()
		)
	)

def load(fileName):
	with open(fileName) as fp:
		global imagedict
		level = json.load(fp)
		imagedict = _makeImages(level["images"])
		
		_makePlayer(**level["player"])
		
		for wall in level.get("walls", []):
			_makeEjector(CHL.ejectID, **wall)
		
		return imagedict[level["background"]]

def _makePlayer(image, x, y):
	global imagedict
	img = imagedict[image]
	rect = Rect(img.get_rect())
	
	EntID, ImageID, RectID = Entity.createPlayer(img, rect, (x, y))
	
	Velocity.register(EntID)
	Accel.register(EntID)
	Accel.store(EntID, 0, 0.8 / 1000)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	Collision.register(EntID)
	
	return EntID

def _makeEjector(ejectHandler, image, x, y):
	global imagedict
	img = imagedict[image]
	rect = Rect(img.get_rect())
	
	EntID, ImageID, RectID = Entity.create(img, rect, (x, y))
	
	Collision.register(EntID)
	Collision.store(EntID, ejectHandler, ejectHandler, 0)
