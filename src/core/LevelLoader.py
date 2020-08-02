#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

# Copyright (C) 2020 Stephen Fedele <32551324+strangeprogrammer@users.noreply.github.com>
# 
# This file is part of Fruit Punch.
# 
# Fruit Punch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Fruit Punch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Fruit Punch.  If not, see <https://www.gnu.org/licenses/>.
# 
# Additional terms apply to this file.  Read the file 'LICENSE.txt' for
# more information.



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
	Layer,
	ImageLoader,
)

imageIDs = {}
imageProps = {}

def _makeImages(images):
	global imageIDs, imageProps
	
	for k, v in images.items():
		imageIDs[k] = ImageLoader.create(
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
	
	Layer.register(EntID)
	Layer.store(EntID, *entity["z"])
	
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
		R.RR.flush()
		
		return R.IR[imageIDs[level["background"]]]
