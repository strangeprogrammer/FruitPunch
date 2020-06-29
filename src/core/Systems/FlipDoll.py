#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G

toDollQuery = None

from .. import Component as C

def init():
	global toDollQuery
	
	toDollQuery = sqa.select([
		C.FDC.c.ChildID,
		C.FC.c.FlipX,
		C.FC.c.FlipY,
		C.FDC.c.OffX,
		C.FDC.c.OffY,
	]).select_from(
		C.FC.join(C.FDC, C.FC.c.EntID == C.FDC.c.EntID)
	).compile()

def register(EntID, ChildID):
	# TODO: Find out whether or not the entity being registered is in a chain of dolls, and assign to it its generation number as appropriate
	# The entity being registered should already be registered with the Flip System
#	try:
#		Generation = G.CONN.execute(
#			sqa.select([
#				C.FDC.c.Generation
#			]).select_from(C.FDC).where(
#				C.FDC.c.ChildID == EntID
#			)
#		).fetchone()[0]
#	except Exception:
#		Generation = 0
	
	G.CONN.execute(
		C.FDC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
#			"Generation": Generation,
			"OffX": False,
			"OffY": False,
		}
	)

def instances(ChildID):
	return len(G.CONN.execute(
		C.FDC.select().where(C.FDC.c.ChildID == ChildID)
	).fetchall())

def deregister(ChildID):
	G.CONN.execute(
		C.FDC.delete().where(C.FDC.c.ChildID == ChildID)
	)

def fetch(ChildID):
	return G.CONN.execute(
		sqa.select([
			C.FDC.c.OffX,
			C.FDC.c.OffY,
		]).select_from(C.FDC).where(
			C.FDC.c.ChildID == ChildID
		)
	).fetchone()

def store(ChildID, OffX, OffY):
	G.CONN.execute(
		C.FDC.update().where(C.FDC.c.ChildID == ChildID), {
			"OffX": OffX,
			"OffY": OffY,
		}
	)

def update():
	# TODO: Implement update in phases based upon generation number
	for ChildID, FlipX, FlipY, OffX, OffY in G.CONN.execute(toDollQuery).fetchall():
		G.CONN.execute(
			C.FC.update().where(C.FC.c.EntID == ChildID),
			{
				"FlipX": bool(FlipX) ^ bool(OffX),
				"FlipY": bool(FlipY) ^ bool(OffY),
			}
		)
