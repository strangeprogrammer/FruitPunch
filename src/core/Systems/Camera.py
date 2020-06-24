#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from .. import Component as C
from .. import Resource as R

from .. import G

from . import Position
from . import Velocity

EntID = RectID = None

def init():
	G.SCREEN = pg.display.set_mode()
	
	G.BGD = G.SCREEN.copy()
	pg.display.flip()
	
	global EntID, RectID
	RectID = R.RR.append(pg.Rect(0, 0, 0, 0))
	
	from .. import Entity
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

def get():
	global RectID
	rect = R.RR[RectID]
	return (rect.left, rect.top)

def set(left, top):
	global RectID
	rect = R.RR[RectID]
	rect.left = left
	rect.top = top

def update(scene):
	global RectID
	rect = R.RR[RectID]
	G.SCREEN.fill( (0, 0, 0) )
	G.SCREEN.blit(scene, rect)
	pg.display.flip()
