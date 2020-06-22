#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa
import math

from .. import G
from .. import Misc

rotateQuery = None

from .. import Component as C
from . import Rotation

def init():
	global rotateQuery
	
	rotateQuery = sqa.select([
		C.RVC.c.EntID,
		C.RVC.c.Omega,
	]).select_from(
		C.RVC
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
	return Misc.degToRad(
		G.CONN.execute(
			sqa	.select([C.RVC.c.Omega]) \
				.select_from(C.RVC) \
				.where(C.RVC.c.EntID == EntID)
		).fetchone()[0]
	)

def set(EntID, Omega):
	G.CONN.execute(
		C.RVC.update().where(C.RVC.c.EntID == EntID), {
			"Omega": Misc.radToDeg(Omega),
		}
	)

def update(dt): # TODO: Re-write this using an execute-many style
	global rotateQuery
	
	for EntID, Omega in G.CONN.execute(rotateQuery).fetchall():
		Theta = Rotation.get(EntID)
		newTheta = Theta + Misc.degToRad(Omega) * dt
		Rotation.set(EntID, newTheta)
