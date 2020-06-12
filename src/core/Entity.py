#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from itertools import count

from . import Component
from . import Resource
from . import G

from .Systems import Velocity

entCounter = None
rectCounter = None
imageCounter = None

def init():
	global entCounter
	entCounter = count()

@Resource.require("RectRes")
@Resource.require("ImageRes")
@Component.require("PosComp")
@Component.require("RectComp")
@Component.require("ImageComp")
@Component.require("AllMove")
@Component.require("AllRects")
@Component.require("AllImages")
@Component.require("AllEnts")
def create(E, I, R, M, IC, RC, PC, IR, RR, image, rect, center):
	rect.center = center
	
	global entCounter
	EntID = next(entCounter)
	ImageID = IR.append(image)
	RectID = RR.append(rect)
	
	G.CONN.execute(E.insert().values(EntID = EntID))
	G.CONN.execute(I.insert().values(ImageID = ImageID))
	G.CONN.execute(R.insert().values(RectID = RectID))
	
	G.CONN.execute(IC.insert().values(EntID = EntID, ImageID = ImageID))
	G.CONN.execute(RC.insert().values(EntID = EntID, RectID = RectID))
	G.CONN.execute(PC.insert().values(EntID = EntID, PosX = center[0], PosY = center[1]))
	
	return EntID, ImageID, RectID

@Component.require("PlayerComp")
def createPlayer(PC, image, rect, center):
	EntID, ImageID, RectID = create(image, rect, center)
	G.CONN.execute(PC.insert().values(EntID = EntID))
	return EntID, ImageID, RectID
