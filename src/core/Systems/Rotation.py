#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa
import math

from .. import G
from .. import Misc

exemptQuery = None
rotateQuery = None
collectable = []

from .. import Component as C
from .. import Resource as R

def init():
	global exemptQuery, rotateQuery
	
	exemptQuery = C.DC.select().where(
		C.DC.c.EntID.notin_(
			sqa.select([C.ROTC.c.EntID]).select_from(C.ROTC)
		)
	).compile()
	
	rotateQuery = sqa.select([
		C.DC.c.EntID,
		C.DC.c.ImageID,
		C.ROTC.c.Theta,
	]).select_from(
		C.DC.join(C.ROTC, C.DC.c.EntID == C.ROTC.c.EntID)
	).compile()

def register(EntID):
	G.CONN.execute(
		C.ROTC.insert(), {
			"EntID": EntID,
			"Theta": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.ROTC.select().where(C.ROTC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.ROTC	.delete() \
			.where(C.ROTC.EntID == EntID)
	)

def fetch(EntID):
	return Misc.degToRad(
		G.CONN.execute(
			sqa	.select([C.ROTC.c.Theta]) \
				.select_from(C.ROTC) \
				.where(C.ROTC.c.EntID == EntID)
		).fetchone()[0]
	)

def store(EntID, Theta):
	G.CONN.execute(
		C.ROTC.update().where(
			C.ROTC.c.EntID == EntID
		), {
			"Theta": Misc.radToDeg(Theta)
		}
	)

def collect():
	global collectable
	for rotateID in collectable:
		del R.IR[rotateID]
		G.CONN.execute(
			C.I	.delete() \
				.where(C.I.c.ImageID == rotateID)
		)
	
	collectable = []

def render():
	global exemptQuery, rotateQuery, collectable
	
	result = G.CONN.execute(exemptQuery).fetchall()
	
	for EntID, ImageID, Theta in G.CONN.execute(rotateQuery).fetchall():
		rotateID = R.IR.append(
			pg.transform.rotate(R.IR[ImageID], Theta)
		)
		
		G.CONN.execute(
			C.I.insert(),
			{"ImageID": rotateID}
		)
		
		collectable.append(rotateID)
		
		result.append({
			"EntID": EntID,
			"ImageID": rotateID,
		})
	
	return result
