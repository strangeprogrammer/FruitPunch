#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from itertools import count

from . import G

from .Systems import Velocity

entCounter = None

from . import Component as C
from . import Resource as R

from .Systems import Position

def init():
	global entCounter
	entCounter = count()

def create(image, rect, center):
	rect.center = center
	
	global entCounter
	EntID = next(entCounter)
	ImageID = R.IR.append(image)
	RectID = R.RR.append(rect)
	
	G.CONN.execute(C.E.insert().values(EntID = EntID))
	G.CONN.execute(C.I.insert().values(ImageID = ImageID))
	G.CONN.execute(C.R.insert().values(RectID = RectID))
	
	G.CONN.execute(C.IC.insert().values(EntID = EntID, ImageID = ImageID))
	G.CONN.execute(C.RECC.insert().values(EntID = EntID, RectID = RectID))
	Position.register(EntID)
	Position.store(EntID, center[0], center[1])
	
	return EntID, ImageID, RectID

def createPlayer(image, rect, center):
	EntID, ImageID, RectID = create(image, rect, center)
	G.CONN.execute(C.PLYC.insert().values(EntID = EntID))
	return EntID, ImageID, RectID
