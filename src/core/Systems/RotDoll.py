#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa
import math

from .. import G
from .. import Component
from ..Component import require as require
from .. import Resource

toDollQuery = None

@require("RotDollComp")
@require("RotationComp")
def init(RC, RDC):
	global toDollQuery
	
	toDollQuery = sqa.select([
		RDC.c.ChildID,
		RC.c.Theta,
		RDC.c.dTheta,
	]).select_from(
		RC.join(RDC, RC.c.EntID == RDC.c.EntID)
	).compile()

@require("RotDollComp")
def register(RDC, EntID, ChildID):
	# TODO: Find out whether or not the entity being registered is in a chain of dolls, and assign to it its generation number as appropriate
	# The entity being registered should already be registered with the Rotation System
	G.CONN.execute(
		RDC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
#			"Generation": Generation,
			"dTheta": 0
		}
	)

@require("RotDollComp")
def instances(RDC, ChildID):
	return len(G.CONN.execute(
		RDC.select().where(RDC.c.ChildID == ChildID)
	).fetchall())

@require("RotDollComp")
def deregister(RDC, ChildID):
	G.CONN.execute(
		RDC.delete().where(RDC.c.ChildID == ChildID)
	)

@require("RotDollComp")
def get(RDC, ChildID):
	return G.CONN.execute(
		sqa.select([
			RDC.c.dTheta,
		]).select_from(RDC).where(
			RDC.c.ChildID == ChildID
		)
	).fetchone()[0] * math.tau / 360

@require("RotDollComp")
def set(RDC, ChildID, dTheta):
	G.CONN.execute(
		RDC.update().where(RDC.c.ChildID == ChildID), {
			"dTheta": dTheta * 360 / math.tau
		}
	)

@require("RotationComp")
def update(RC):
	# TODO: Implement update in phases based upon generation number
	for ChildID, Theta, dTheta in G.CONN.execute(toDollQuery).fetchall():
		G.CONN.execute(
			RC.update().where(RC.c.EntID == ChildID),
			{
				"Theta": Theta + dTheta
			}
		)
