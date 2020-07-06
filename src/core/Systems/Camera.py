#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from .. import Component as C
from .. import Resource as R

from .. import G
from ..Misc import Rect
from .. import Entity

from . import Position
from . import Velocity
from . import Rectangle

EntID = RectID = BindID = None

def init():
	global EntID, RectID
	
	G.SCREEN = pg.display.set_mode()
	rect = Rect(G.SCREEN.get_rect())
	(rect.x, rect.y) = (0, 0)
	RectID = R.RR.append(rect)
	
	EntID = next(Entity.entCounter)
	
	G.CONN.execute(
		C.E.insert(), {
			"EntID": EntID,
		}
	)
	
	Rectangle.register(EntID)
	Rectangle.store(EntID, RectID)
	
	Position.register(EntID)
	Velocity.register(EntID)

def fetch():
	global RectID
	rect = R.RR[RectID]
	return (rect.left, rect.top)

def store(left, top):
	global RectID
	rect = R.RR[RectID]
	rect.left = left
	rect.top = top

def bind(EntID):
	global BindID
	BindID = EntID

def unbind():
	global BindID
	BindID = None

def update():
	global RectID, BindID
	if BindID is not None:
		R.RR[RectID].center = R.RR[Rectangle.fetch(BindID)].center
