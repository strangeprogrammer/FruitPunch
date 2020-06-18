#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G
from ..Component import require

updateQuery = None

@require("StrutBaseComp")
@require("PosComp")
def init(PC, SBC):
	global updateQuery
	updateQuery = sqa.select([
		SBC.c.ChildID,
		PC.c.PosX,
		PC.c.PosY,
		SBC.c.OffX,
		SBC.c.OffY,
	]).select_from(
		PC.join(SBC, PC.c.EntID == SBC.c.EntID)
	).compile()

@require("StrutBaseComp")
def register(SBC, EntID, ChildID):
	G.CONN.execute(
		SBC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
			"OffX": 0,
			"OffY": 0,
		}
	)

@require("StrutBaseComp")
def instances(SBC, ChildID):
	return len(G.CONN.execute(
		SBC.select().where(SBC.c.ChildID == ChildID)
	).fetchall())

@require("StrutBaseComp")
def deregister(SBC, ChildID):
	G.CONN.execute(
		SBC.delete().where(SBC.c.ChildID == ChildID)
	)

@require("StrutBaseComp")
def get(SBC, EntID):
	return G.CONN.execute(
		sqa	.select([SBC.c.OffX, SBC.c.OffY]) \
			.select_from(SBC) \
			.where(SBC.c.ChildID == ChildID)
	).fetchone()

@require("StrutBaseComp")
def set(SBC, ChildID, OffX, OffY):
	G.CONN.execute(
		SBC.update().where(
			SBC.c.ChildID == ChildID,
		), {
			"OffX": OffX,
			"OffY": OffY,
		}
	)

@require("StrutComp")
def _updateStrutComp(SC, values):
	G.CONN.execute(SC.delete())
	if 0 < len(values):
		G.CONN.execute(SC.insert(), values)

@require("StrutBaseComp")
def _resetStrutComp(SBC):
	_updateStrutComp(
		G.CONN.execute(
			SBC.select()
		).fetchall()
	)

@require("PosComp")
def update(PC):
	_resetStrutComp()
	
	global updateQuery
	for ChildID, PosX, PosY, OffX, OffY in G.CONN.execute(updateQuery).fetchall():
		G.CONN.execute(
			PC.update().where(PC.c.EntID == ChildID ), {
				"PosX": PosX + OffX,
				"PosY": PosY + OffY,
			}
		)
