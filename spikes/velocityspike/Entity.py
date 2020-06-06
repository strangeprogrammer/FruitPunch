#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import Component
import Resource
import G

entCounter = None
rectCounter = None
imageCounter = None

def init():
	global entCounter, rectCounter, imageCounter
	from itertools import count
	entCounter = count()
	rectCounter = count()
	imageCounter = count()

@Resource.require("RectRes")
@Resource.require("ImageRes")
@Component.require("VelocityComp")
@Component.require("PositionComp")
@Component.require("RectComp")
@Component.require("ImageComp")
@Component.require("AllMove")
@Component.require("AllRects")
@Component.require("AllImages")
@Component.require("AllEnts")
def create(E, I, R, M, IC, RC, PC, VC, IR, RR, image, rect, center, velocity):
	rect.center = center
	
	global entCounter, rectCounter, imageCounter
	EntID = next(entCounter)
	RectID = next(rectCounter)
	ImageID = next(imageCounter)
	
	G.CONN.execute(E.insert().values(EntID = EntID))
	G.CONN.execute(I.insert().values(ImageID = ImageID))
	G.CONN.execute(R.insert().values(RectID = RectID))
	G.CONN.execute(M.insert().values(EntID = EntID))
	
	G.CONN.execute(IC.insert().values(EntID = EntID, ImageID = ImageID))
	G.CONN.execute(RC.insert().values(EntID = EntID, RectID = RectID))
	G.CONN.execute(PC.insert().values(RectID = RectID, PosX = center[0], PosY = center[1]))
	G.CONN.execute(VC.insert().values(RectID = RectID, VelX = velocity[0], VelY = velocity[1]))
	
	IR[ImageID] = image
	RR[RectID] = rect
	
	return EntID, RectID, ImageID

@Component.require("PlayerComp")
def createPlayer(PC, image, rect, center, velocity):
	EntID = create(image, rect, center, velocity)[0]
	G.CONN.execute(PC.insert().values(EntID = EntID))
