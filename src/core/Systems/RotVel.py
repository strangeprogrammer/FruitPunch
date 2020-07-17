#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa
import math

from .. import G
from .. import Misc
from .. import Time

from .. import Component as C

from . import Rotation

rotateQuery = None

def init():
	global rotateQuery
	
	rotateQuery = sqa.select([
		C.RVC.c.EntID,
		C.RVC.c.Omega,
	]).select_from(
		C.RVC
	).compile()

def quit():
	G.CONN.execute(
		C.RVC.delete()
	)

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

def fetch(EntID):
	return Misc.degToRad(
		G.CONN.execute(
			sqa	.select([C.RVC.c.Omega]) \
				.select_from(C.RVC) \
				.where(C.RVC.c.EntID == EntID)
		).fetchone()[0]
	)

def store(EntID, Omega):
	G.CONN.execute(
		C.RVC.update().where(C.RVC.c.EntID == EntID), {
			"Omega": Misc.radToDeg(Omega),
		}
	)

def update():
	global rotateQuery
	
	for EntID, Omega in G.CONN.execute(rotateQuery).fetchall():
		Theta = Rotation.fetch(EntID)
		newTheta = Theta + Misc.degToRad(Omega) * Time.elapsed
		Rotation.store(EntID, newTheta)
