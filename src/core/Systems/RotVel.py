#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa
import math

from .. import G

rotateQuery = None

from .. import Component as C

def init():
	global rotateQuery
	
	rotateQuery = sqa.select([
		C.ROTC.c.EntID,
		C.ROTC.c.Theta,
		C.RVC.c.Omega,
	]).select_from(
		C.ROTC.join(C.RVC, C.ROTC.c.EntID == C.RVC.c.EntID)
	).compile()

def register(EntID):
	G.CONN.execute(
		C.RVC.insert(), {
			"EntID": EntID,
			"Omega": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.RVC.select().where(C.RVC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.RVC.delete().where(C.RVC.c.EntID == EntID)
	)

def get(EntID):
	return G.CONN.execute(
		sqa	.select([C.RVC.c.Omega]) \
			.select_from(C.RVC) \
			.where(C.RVC.c.EntID == EntID)
	).fetchone()[0] * math.tau / 360

def set(EntID, Omega):
	G.CONN.execute(
		C.RVC.update().where(C.RVC.c.EntID == EntID), {
			"Omega": Omega * 360 / math.tau,
		}
	)

def update(dt): # TODO: Re-write this using an execute-many style
	global rotateQuery
	
	for EntID, Theta, Omega in G.CONN.execute(rotateQuery).fetchall():
		newTheta = Theta + Omega * dt
		
		G.CONN.execute(
			C.ROTC.update().where(
				C.ROTC.c.EntID == EntID,
			).values(
				Theta = newTheta
			)
		)
