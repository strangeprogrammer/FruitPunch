#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G

movingQuery = None

from .. import Component as C

from . import Position

def init():
	global movingQuery
	
	movingQuery = sqa.select([
		C.VC.c.EntID,
		C.VC.c.VelX,
		C.VC.c.VelY,
	]).select_from(
		C.VC,
	).compile()

def register(EntID):
	G.CONN.execute(
		C.VC.insert().values(EntID = EntID, VelX = 0, VelY = 0)
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.VC.select().where(C.VC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.VC.delete().where(C.VC.c.EntID == EntID)
	)

def get(EntID):
	return G.CONN.execute(
		sqa	.select([C.VC.c.VelX, C.VC.c.VelY]) \
			.select_from(C.VC) \
			.where(C.VC.c.EntID == EntID)
	).fetchone()

def set(EntID, VelX, VelY):
	G.CONN.execute(
		C.VC	.update() \
			.where(C.VC.c.EntID == EntID) \
			.values(VelX = VelX, VelY = VelY)
	)

def update(dt):
	global movingQuery
	
	for EntID, VelX, VelY in G.CONN.execute(movingQuery).fetchall():
		(PosX, PosY) = Position.get(EntID)
		newX = PosX + VelX * dt
		newY = PosY + VelY * dt
		Position.set(EntID, newX, newY)
