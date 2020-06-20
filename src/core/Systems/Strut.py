#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G

updateQuery = None

from .. import Component as C

def init():
	global updateQuery
	
	updateQuery = sqa.select([
		C.SBC.c.ChildID,
		C.POSC.c.PosX,
		C.POSC.c.PosY,
		C.SBC.c.OffX,
		C.SBC.c.OffY,
	]).select_from(
		C.POSC.join(C.SBC, C.POSC.c.EntID == C.SBC.c.EntID)
	).compile()

def register(EntID, ChildID):
	G.CONN.execute(
		C.SBC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
			"OffX": 0,
			"OffY": 0,
		}
	)

def instances(ChildID):
	return len(G.CONN.execute(
		C.SBC.select().where(C.SBC.c.ChildID == ChildID)
	).fetchall())

def deregister(ChildID):
	G.CONN.execute(
		C.SBC.delete().where(C.SBC.c.ChildID == ChildID)
	)

def get(EntID):
	return G.CONN.execute(
		sqa	.select([C.SBC.c.OffX, C.SBC.c.OffY]) \
			.select_from(C.SBC) \
			.where(C.SBC.c.ChildID == ChildID)
	).fetchone()

def set(ChildID, OffX, OffY):
	G.CONN.execute(
		C.SBC.update().where(
			C.SBC.c.ChildID == ChildID,
		), {
			"OffX": OffX,
			"OffY": OffY,
		}
	)

def _updateStrutComp(values):
	G.CONN.execute(C.SC.delete())
	if 0 < len(values):
		G.CONN.execute(C.SC.insert(), values)

def _resetStrutComp():
	_updateStrutComp(
		G.CONN.execute(
			C.SBC.select()
		).fetchall()
	)

def update():
	_resetStrutComp()
	
	global updateQuery
	for ChildID, PosX, PosY, OffX, OffY in G.CONN.execute(updateQuery).fetchall():
		G.CONN.execute(
			C.POSC.update().where(C.POSC.c.EntID == ChildID), {
				"PosX": PosX + OffX,
				"PosY": PosY + OffY,
			}
		)
