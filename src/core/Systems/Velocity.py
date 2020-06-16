#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G
from ..Component import require

movingQuery = None

@require("VelComp")
@require("PosComp")
@require("RectComp")
def init(RC, PC, VC):
	global movingQuery
	
	movingQuery = sqa.select([
		RC.c.EntID,
		RC.c.RectID,
		PC.c.PosX,
		PC.c.PosY,
		VC.c.VelX,
		VC.c.VelY,
	]).select_from(
		RC	.join(PC, RC.c.EntID == PC.c.EntID) \
			.join(VC, PC.c.EntID == VC.c.EntID)
	).compile()

@require("VelComp")
def register(VC, EntID):
	G.CONN.execute(
		VC.insert().values(EntID = EntID, VelX = 0, VelY = 0)
	)

@require("VelComp")
def instances(VC, EntID):
	return len(G.CONN.execute(
		VC.select().where(VC.c.EntID == EntID)
	).fetchall())

@require("VelComp")
def deregister(VC, EntID):
	G.CONN.execute(
		VC.delete().where(VC.c.EntID == EntID)
	)

@require("VelComp")
def get(VC, EntID):
	return G.CONN.execute(
		sqa	.select([VC.c.VelX, VC.c.VelY]) \
			.select_from(VC) \
			.where(VC.c.EntID == EntID)
	).fetchone()

@require("VelComp")
def set(VC, EntID, VelX, VelY):
	G.CONN.execute(
		VC	.update() \
			.where(VC.c.EntID == EntID) \
			.values(VelX = VelX, VelY = VelY)
	)

@require("PosComp")
def update(PC, dt):
	global movingQuery
	for EntID, RectID, PosX, PosY, VelX, VelY in G.CONN.execute(movingQuery).fetchall():
		newX = PosX + VelX * dt
		newY = PosY + VelY * dt
		
		G.CONN.execute(
			PC.update().where(
				PC.c.EntID == EntID,
			).values(
				PosX = newX,
				PosY = newY,
			)
		)
