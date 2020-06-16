#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa
import math

from .. import G
from ..Component import require

rotateQuery = None

@require("RotVelComp")
@require("RotationComp")
def init(RC, RVC):
	global rotateQuery
	
	rotateQuery = sqa.select([
		RC.c.EntID,
		RC.c.Theta,
		RVC.c.Omega,
	]).select_from(
		RC.join(RVC, RC.c.EntID == RVC.c.EntID)
	).compile()

@require("RotVelComp")
def register(RVC, EntID):
	G.CONN.execute(
		RVC.insert(), {
			"EntID": EntID,
			"Omega": 0,
		}
	)

@require("RotVelComp")
def instances(RVC, EntID):
	return len(G.CONN.execute(
		RVC.select().where(RVC.c.EntID == EntID)
	).fetchall())

@require("RotVelComp")
def deregister(RVC, EntID):
	G.CONN.execute(
		RVC.delete().where(RVC.c.EntID == EntID)
	)

@require("RotVelComp")
def get(RVC, EntID):
	return G.CONN.execute(
		sqa	.select([RVC.c.Omega]) \
			.select_from(RVC) \
			.where(RVC.c.EntID == EntID)
	).fetchone()[0] * math.tau / 360

@require("RotVelComp")
def set(RVC, EntID, Omega):
	G.CONN.execute(
		RVC.update().where(RVC.c.EntID == EntID), {
			"Omega": Omega * 360 / math.tau,
		}
	)

@require("RotationComp")
def update(RC, dt): # TODO: Re-write this using an execute-many style
	global rotateQuery
	
	for EntID, Theta, Omega in G.CONN.execute(rotateQuery).fetchall():
		newTheta = Theta + Omega * dt
		
		G.CONN.execute(
			RC.update().where(
				RC.c.EntID == EntID,
			).values(
				Theta = newTheta
			)
		)
