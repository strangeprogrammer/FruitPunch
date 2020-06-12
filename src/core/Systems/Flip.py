#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G

from .. import Component
from ..Component import require as require
from .. import Resource

renderQuery = None

@require("FlipImages")
@require("FlipComp")
@require("DrawComp")
def init(DC, FC, FI):
	global renderQuery
	
	exempt = DC.select().where(
		DC.c.EntID.notin_(
			sqa.select([FC.c.EntID]).select_from(FC)
		)
	)
	
	doFlips = sqa.select([
		DC.c.EntID,
		FI.c.OutImageID,
	]).select_from(
		DC.join(
			FC,
			DC.c.EntID == FC.c.EntID
		).join(
			FI,
			sqa.and_(
				DC.c.ImageID == FI.c.InImageID,
				FC.c.FlipX == FI.c.FlipX,
				FC.c.FlipY == FI.c.FlipY,
			)
		)
	)
	
	renderQuery = exempt.union(doFlips).compile()

@require("FlipComp")
def register(FC, EntID):
	G.CONN.execute(
		FC.insert(), {
			"EntID": EntID,
			"FlipX": False,
			"FlipY": False,
		}
	)

@require("FlipComp")
def numregistered(FC, EntID):
	return len(G.CONN.execute(
		FC.select().where(FC.c.EntID == EntID)
	).fetchall())

@require("FlipComp")
def deregister(FC, EntID):
	G.CONN.execute(
		FC	.delete()
			.where(FC.EntID == EntID)
	)

@require("FlipComp")
def get(FC, EntID):
	return G.CONN.execute(
		sqa	.select([FC.c.FlipX, FC.c.FlipY]) \
			.select_from(FC) \
			.where(FC.c.EntID == EntID)
	).fetchone()

@require("FlipComp")
def set(FC, EntID, FlipX, FlipY):
	G.CONN.execute(
		FC.update().where(
			FC.c.EntID == EntID
		), {
			"FlipX": FlipX,
			"FlipY": FlipY,
		}
	)

# TODO: Make this function obsolete by automatically registering images whenever an entity is registered
@Resource.require("ImageRes")
@require("FlipImages")
@require("AllImages")
def registerImage(I, FI, IR, ImageID):
	noflipped = ImageID
	xflipped = IR.append(
		pg.transform.flip(IR[ImageID], True, False)
	)
	yflipped = IR.append(
		pg.transform.flip(IR[ImageID], False, True)
	)
	xyflipped = IR.append(
		pg.transform.flip(IR[ImageID], True, True)
	)
	
	G.CONN.execute(
		FI.insert(), [
			{"InImageID": ImageID, "FlipX": False,	"FlipY": False,	"OutImageID": ImageID},
			{"InImageID": ImageID, "FlipX": True,	"FlipY": False,	"OutImageID": xflipped},
			{"InImageID": ImageID, "FlipX": False,	"FlipY": True,	"OutImageID": yflipped},
			{"InImageID": ImageID, "FlipX": True,	"FlipY": True,	"OutImageID": xyflipped},
		]
	)
	
	G.CONN.execute(
		I.insert(), [
			# We assume 'ImageID' has already been registered
			{"ImageID": xflipped},
			{"ImageID": yflipped},
			{"ImageID": xyflipped},
		]
	)

def render():
	global renderQuery
	return G.CONN.execute(renderQuery).fetchall()
