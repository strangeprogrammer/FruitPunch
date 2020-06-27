#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from .. import Component as C
from .. import Resource as R

from .. import G

from . import Position
from . import Velocity

screen = EntID = RectID = None

def init():
	global screen, EntID, RectID
	
	screen = pg.display.set_mode()
	rect = screen.get_rect()
	(rect.x, rect.y) = (0, 0)
	RectID = R.RR.append(rect)
	
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
	global screen, RectID
	rect = R.RR[RectID].copy()
	rect.x = -rect.x
	rect.y = -rect.y
	screen.blit(scene, rect)
	pg.display.flip()
