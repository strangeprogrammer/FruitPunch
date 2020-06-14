#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa
import math

from .. import G

from .. import Component
from ..Component import require as require
from .. import Resource

exemptQuery = None
rotateQuery = None
collectable = []

@require("RotationComp")
@require("DrawComp")
def init(DC, RC):
	global exemptQuery, rotateQuery
	
	exemptQuery = DC.select().where(
		DC.c.EntID.notin_(
			sqa.select([RC.c.EntID]).select_from(RC)
		)
	).compile()
	
	rotateQuery = sqa.select([
		DC.c.EntID,
		DC.c.ImageID,
		RC.c.Theta,
	]).select_from(
		DC.join(RC, DC.c.EntID == RC.c.EntID)
	).compile()

@require("RotationComp")
def register(RC, EntID):
	G.CONN.execute(
		RC.insert(), {
			"EntID": EntID,
			"Theta": 0,
		}
	)

@require("RotationComp")
def instances(RC, EntID):
	return len(G.CONN.execute(
		RC.select().where(RC.c.EntID == EntID)
	).fetchall())

@require("RotationComp")
def deregister(RC, EntID):
	G.CONN.execute(
		RC	.delete()
			.where(RC.EntID == EntID)
	)

@require("RotationComp")
def get(RC, EntID):
	return G.CONN.execute(
		sqa	.select([RC.c.Theta]) \
			.select_from(RC) \
			.where(RC.c.EntID == EntID)
	).fetchone()[0] * math.tau / 360

@require("RotationComp")
def set(RC, EntID, Theta):
	G.CONN.execute(
		RC.update().where(
			RC.c.EntID == EntID
		), {"Theta": Theta * 360 / math.tau}
	)

@Resource.require("ImageRes")
@require("AllImages")
def collect(I, IR):
	global collectable
	for rotateID in collectable:
		del IR[rotateID]
		G.CONN.execute(
			I	.delete() \
				.where(I.c.ImageID == rotateID)
		)
	
	collectable = []

@Resource.require("ImageRes")
@require("RotationComp")
@require("DrawComp")
@require("AllImages")
def render(I, DC, RC, IR):
	global exemptQuery, rotateQuery, collectable
	
	result = G.CONN.execute(exemptQuery).fetchall()
	
	for EntID, ImageID, Theta in G.CONN.execute(rotateQuery).fetchall():
		rotateID = IR.append(
			pg.transform.rotate(IR[ImageID], Theta)
		)
		
		G.CONN.execute(
			I.insert(),
			{"ImageID": rotateID}
		)
		
		collectable.append(rotateID)
		
		result.append({
			"EntID": EntID,
			"ImageID": rotateID,
		})
	
	return result
