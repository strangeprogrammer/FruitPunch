#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G

rectPosQuery = None

from .. import Component as C
from .. import Resource as R

def init():
	global rectPosQuery
	
	rectPosQuery = sqa.select([
		C.RECC.c.RectID,
		C.POSC.c.PosX,
		C.POSC.c.PosY,
	]).select_from(
		C.RECC.join(C.POSC, C.RECC.c.EntID == C.POSC.c.EntID)
	).compile()

def register(EntID):
	G.CONN.execute(
		C.POSC.insert(), {
			"EntID": EntID,
			"PosX": 0,
			"PosY": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.POSC.select().where(C.POSC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.POSC.delete().where(C.POSC.c.EntID == EntID)
	)

def get(EntID):
	return G.CONN.execute(
		sqa	.select([C.POSC.c.PosX, C.POSC.c.PosY]) \
			.select_from(C.POSC) \
			.where(C.POSC.c.EntID == EntID)
	).fetchone()

def set(EntID, PosX, PosY):
	G.CONN.execute(
		C.POSC	.update() \
			.where(C.POSC.c.EntID == EntID), {
			"PosX": PosX,
			"PosY": PosY,
		}
	)

def update():
	global rectPosQuery
	
	for RectID, PosX, PosY in G.CONN.execute(rectPosQuery).fetchall():
		R.RR[RectID].center = (PosX, PosY)
