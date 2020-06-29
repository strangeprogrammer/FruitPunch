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

EntID = RectID = None

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
	G.CONN.execute(
		C.RECC.insert(), {
			"EntID": EntID,
			"RectID": RectID,
		}
	)
	
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
