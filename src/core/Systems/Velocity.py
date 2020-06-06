#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G
from .. import Component
from .. import Resource

movingQuery = None

@Component.require("VelocityComp")
@Component.require("PositionComp")
@Component.require("RectComp")
@Component.require("AllMove")
def init(M, RC, PC, VC):
	global movingQuery
	movingQuery = sqa.select([
		RC.c.RectID,
		PC.c.PosX,
		PC.c.PosY,
		VC.c.VelX,
		VC.c.VelY,
	]).select_from(
		M	.join(RC, M.c.EntID == RC.c.EntID) \
			.join(PC, RC.c.RectID == PC.c.RectID) \
			.join(VC, PC.c.RectID == VC.c.RectID)
	).compile()

@Resource.require("RectRes")
@Component.require("PositionComp")
def update(PC, RR, dt):
	global movingQuery
	for RectID, PosX, PosY, VelX, VelY in G.CONN.execute(movingQuery).fetchall():
		newX = PosX + VelX * dt
		newY = PosY + VelY * dt
		G.CONN.execute(
			PC.update().where(
				PC.c.RectID == RectID,
			).values(
				PosX = newX,
				PosY = newY,
			)
		)
		RR[RectID].center = (newX, newY)
