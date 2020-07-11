#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from itertools import count

from . import G

from .Systems import Velocity

entCounter = None

from . import Component as C
from . import Resource as R

from .Systems import Position
from .Systems import Rectangle
from .Systems import Image

def create(image, rect, topleft):
	rect.topleft = topleft
	
	EntID = R.ER.append(None)
	ImageID = R.IR.append(image)
	RectID = R.RR.append(rect)
	
	G.CONN.execute(C.E.insert().values(EntID = EntID))
	G.CONN.execute(C.I.insert().values(ImageID = ImageID))
	G.CONN.execute(C.R.insert().values(RectID = RectID))
	
	Image.register(EntID)
	Image.store(EntID, ImageID)
	
	Rectangle.register(EntID)
	Rectangle.store(EntID, RectID)
	
	Position.register(EntID)
	Position.store(EntID, *rect.center)
	
	return EntID, ImageID, RectID

def createPlayer(image, rect, center):
	EntID, ImageID, RectID = create(image, rect, center)
	G.CONN.execute(C.PLYC.insert().values(EntID = EntID))
	return EntID, ImageID, RectID
