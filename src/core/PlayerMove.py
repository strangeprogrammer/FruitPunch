#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from . import G
from . import Component
from . import Events

"""
Every time an important button is pressed, the following SQL is run (with X and Y based upon what button's been pressed):

	UPDATE	VelocityComp
	SET	VelX = VelX + X, VelY = VelY + Y
	WHERE	VelocityComp.RectID IN (
		SELECT RectID
		FROM PlayerComp INNER JOIN RectComp );
"""

velUpdate = None

@Component.require("VelocityComp")
def moveHandler(VC, e):
	(X, Y) = (0, 0)
	
	if e.key == pg.K_UP:
		Y -= 0.1
	elif e.key == pg.K_DOWN:
		Y += 0.1
	elif e.key == pg.K_LEFT:
		X -= 0.1
	elif e.key == pg.K_RIGHT:
		X += 0.1
	
	global velUpdate
	G.CONN.execute(velUpdate.values(VelX = VC.c.VelX + X, VelY = VC.c.VelY + Y))

@Component.require("VelocityComp")
@Component.require("RectComp")
@Component.require("PlayerComp")
def init(PC, RC, VC):
	Events.register(pg.KEYDOWN, moveHandler)
	
	global velUpdate
	velUpdate = VC.update().where(VC.c.RectID.in_(
		sqa.select(
			[RC.c.RectID]
		).select_from(
			RC.join(PC, RC.c.EntID == PC.c.EntID))
		)
	)
