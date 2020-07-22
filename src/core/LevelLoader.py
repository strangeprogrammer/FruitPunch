#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import json
import math
import pygame as pg

from . import G
from . import CollHandLib as CHL
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
	Flip,
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

def _makeEntImage(EntID, entity):
	if "image" in entity:
		global imageIDs
		ImageID = imageIDs[entity["image"]]
		
		Image.register(EntID)
		Image.store(EntID, ImageID)
		
		return R.IR[ImageID].get_rect()
	else:
		return None

def _makeEntRect(EntID, entity, rect = None):
	if rect is None:
		rect = Rect(0, 0, entity["width"], entity["height"])
	
	rect.topleft = [entity["x"], entity["y"]]
	
	RectID = R.RR.append(rect)
	
	Rectangle.register(EntID)
	Rectangle.store(EntID, RectID)
	
	return rect

def _makeEntPlayer(EntID):
	G.CONN.execute(C.PLYC.insert().values(EntID = EntID))
	
	Flip.registerImage(Image.fetch(EntID))
	Flip.register(EntID)
	
	Velocity.register(EntID)
	Accel.register(EntID)
	Accel.store(EntID, 0, 0.8 / 1000)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	Collision.registerU(EntID)

def _makeEntWall(EntID, entity):
	eject = entity["eject"]
	
	if "up" in eject:
		Collision.registerT(EntID, CHL.onEjectUpID, CHL.offEjectUpID)
	if "down" in eject:
		Collision.registerT(EntID, CHL.onEjectDownID, CHL.offEjectDownID)
	if "left" in eject:
		Collision.registerT(EntID, CHL.onEjectLeftID, CHL.offEjectLeftID)
	if "right" in eject:
		Collision.registerT(EntID, CHL.onEjectRightID, CHL.offEjectRightID)

def _makeEntPlatform(EntID, entity):
	eject = entity["eject"]
	
	if "up" in eject:
		Collision.registerT(EntID, CHL.onOneWayUpID, CHL.offOneWayUpID)
	if "down" in eject:
		Collision.registerT(EntID, CHL.onOneWayDownID, CHL.offOneWayDownID)
	if "left" in eject:
		Collision.registerT(EntID, CHL.onOneWayLeftID, CHL.offOneWayLeftID)
	if "right" in eject:
		Collision.registerT(EntID, CHL.onOneWayRightID, CHL.offOneWayRightID)

def _makeEntDoor(EntID, entity):
	R.AAR[EntID] = {
		"filename": entity["levelRef"]
	}
	
	Collision.registerT(EntID, CHL.onDoorID, 0)

def _makeEntity(entity):
	EntID = R.ER.append(None)
	
	rect = _makeEntImage(EntID, entity)
	rect = _makeEntRect(EntID, entity, rect = rect)
	
	Position.register(EntID)
	Position.store(EntID, *rect.center)
	
	if entity["type"] == "player":
		_makeEntPlayer(EntID)
		return
	elif entity["type"] == "wall":
		_makeEntWall(EntID, entity)
		return
	elif entity["type"] == "platform":
		_makeEntPlatform(EntID, entity)
		return
	elif entity["type"] == "door":
		_makeEntDoor(EntID, entity)
		return

def load(fileName):
	with open(fileName) as fp:
		level = json.load(fp)
		_makeImages(level["images"])
		
		for entity in level.get("entities", []):
			_makeEntity(entity)
		
		R.ER.flush()
		R.IR.flush()
		R.RR.flush()
		
		return R.IR[imageIDs[level["background"]]]
