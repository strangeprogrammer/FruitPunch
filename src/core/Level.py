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
	Image,
	Rectangle,
	Position,
	Velocity,
	Accel,
	Rotation,
	RotVel,
	Collision,
)

imageIDs = {}
imageProps = {}

def _loadImage(fileName, width = None, height = None):
	base = pg.image.load(
		fileName
	).convert_alpha()
	
	base_rect = base.get_rect()
	
	if width is not None and height is not None:
		base = pg.transform.scale(base, (width, height))
	elif width is not None and height is None:
		base = pg.transform.scale(base, (width, base_rect.height))
	elif width is None and height is not None:
		base = pg.transform.scale(base, (base_rect.width, height))
	
	ImageID = R.IR.append(base)
	
	return ImageID

def _makeImages(images):
	global imageIDs, imageProps
	
	for k, v in images.items():
		imageIDs[k] = _loadImage(
			v["path"],
			v.get("width", None),
			v.get("height", None),
		)
		imageProps[k] = v

def _makePlayer(x, y, image = None):
	global imageIDs
	ImageID = imageIDs[image]
	img = R.IR[ImageID]
	rect = Rect(img.get_rect())
	
	EntID, ImageID, RectID = Entity.createPlayer(img, rect, (x, y))
	
	Velocity.register(EntID)
	Accel.register(EntID)
	Accel.store(EntID, 0, 0.8 / 1000)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	Collision.registerU(EntID)
	
	return EntID

def _makeEjector(rect, eject = []):
	EntID = R.ER.append(None)
	RectID = R.RR.append(rect)
	
	Rectangle.register(EntID)
	Rectangle.store(EntID, RectID)
	
	Position.register(EntID)
	Position.store(EntID, *rect.center)
	
	if "up" in eject:
		Collision.registerT(EntID, CHL.onEjectUpID, CHL.offEjectUpID)
	if "down" in eject:
		Collision.registerT(EntID, CHL.onEjectDownID, CHL.offEjectDownID)
	if "left" in eject:
		Collision.registerT(EntID, CHL.onEjectLeftID, CHL.offEjectLeftID)
	if "right" in eject:
		Collision.registerT(EntID, CHL.onEjectRightID, CHL.offEjectRightID)
	
	return EntID

def _makeWall(x, y, eject = [], image = None, width = None, height = None, name = None):
	global imageIDs
	
	if image is not None:
		ImageID = imageIDs[image]
		rect = R.IR[ImageID].get_rect()
		rect.topleft = (x, y)
	else:
		assert width is not None, "A width must be specified for the imageless entity with name: " + str(name)
		assert height is not None, "A height must be specified for the imageless entity with name: " + str(name)
		
		rect = Rect(x, y, width, height)
	
	EntID = _makeEjector(rect, eject)
	
	if image is not None:
		Image.register(EntID)
		Image.store(EntID, ImageID)

def _makeOneWay(rect, eject = []):
	EntID = R.ER.append(None)
	RectID = R.RR.append(rect)
	
	Rectangle.register(EntID)
	Rectangle.store(EntID, RectID)
	
	Position.register(EntID)
	Position.store(EntID, *rect.center)
	
	if "up" in eject:
		Collision.registerT(EntID, CHL.onOneWayUpID, CHL.offOneWayUpID)
	if "down" in eject:
		Collision.registerT(EntID, CHL.onOneWayDownID, CHL.offOneWayDownID)
	if "left" in eject:
		Collision.registerT(EntID, CHL.onOneWayLeftID, CHL.offOneWayLeftID)
	if "right" in eject:
		Collision.registerT(EntID, CHL.onOneWayRightID, CHL.offOneWayRightID)
	
	return EntID

def _makePlatform(x, y, eject = [], image = None, width = None, height = None, name = None):
	global imageIDs
	
	if image is not None:
		ImageID = imageIDs[image]
		rect = R.IR[ImageID].get_rect()
		rect.topleft = (x, y)
	else:
		assert width is not None, "A width must be specified for the imageless entity with name: " + str(name)
		assert height is not None, "A height must be specified for the imageless entity with name: " + str(name)
		
		rect = Rect(x, y, width, height)
	
	EntID = _makeOneWay(rect, eject)
	
	if image is not None:
		Image.register(EntID)
		Image.store(EntID, ImageID)

def load(fileName):
	with open(fileName) as fp:
		level = json.load(fp)
		_makeImages(level["images"])
		
		_makePlayer(**level["player"])
		
		for wall in level.get("walls", []):
			_makeWall(**wall)
		
		for platform in level.get("platforms", []):
			_makePlatform(**platform)
		
		return R.IR[imageIDs[level["background"]]]
