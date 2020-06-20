#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa
import math

from .. import G

toDollQuery = None

from .. import Component as C

def init():
	global toDollQuery
	
	toDollQuery = sqa.select([
		C.RDC.c.ChildID,
		C.ROTC.c.Theta,
		C.RDC.c.dTheta,
	]).select_from(
		C.ROTC.join(C.RDC, C.ROTC.c.EntID == C.RDC.c.EntID)
	).compile()

def register(EntID, ChildID):
	# TODO: Find out whether or not the entity being registered is in a chain of dolls, and assign to it its generation number as appropriate
	# The entity being registered should already be registered with the Rotation System
	G.CONN.execute(
		C.RDC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
#			"Generation": Generation,
			"dTheta": 0
		}
	)

def instances(ChildID):
	return len(G.CONN.execute(
		C.RDC.select().where(C.RDC.c.ChildID == ChildID)
	).fetchall())

def deregister(ChildID):
	G.CONN.execute(
		C.RDC.delete().where(C.RDC.c.ChildID == ChildID)
	)

def get(ChildID):
	return G.CONN.execute(
		sqa.select([
			C.RDC.c.dTheta,
		]).select_from(C.RDC).where(
			C.RDC.c.ChildID == ChildID
		)
	).fetchone()[0] * math.tau / 360

def set(ChildID, dTheta):
	G.CONN.execute(
		C.RDC.update().where(C.RDC.c.ChildID == ChildID), {
			"dTheta": dTheta * 360 / math.tau
		}
	)

def update():
	# TODO: Implement update in phases based upon generation number
	for ChildID, Theta, dTheta in G.CONN.execute(toDollQuery).fetchall():
		G.CONN.execute(
			C.ROTC.update().where(C.ROTC.c.EntID == ChildID),
			{
				"Theta": Theta + dTheta
			}
		)
