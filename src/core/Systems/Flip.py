#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G

renderQuery = None

from .. import Component as C
from .. import Resource as R

def init():
	global renderQuery
	
	exempt = C.DC.select().where(
		C.DC.c.EntID.notin_(
			sqa.select([C.FC.c.EntID]).select_from(C.FC)
		)
	)
	
	doFlips = sqa.select([
		C.DC.c.EntID,
		C.FI.c.OutImageID,
	]).select_from(
		C.DC.join(
			C.FC,
			C.DC.c.EntID == C.FC.c.EntID
		).join(
			C.FI,
			sqa.and_(
				C.DC.c.ImageID == C.FI.c.InImageID,
				C.FC.c.FlipX == C.FI.c.FlipX,
				C.FC.c.FlipY == C.FI.c.FlipY,
			)
		)
	)
	
	renderQuery = exempt.union(doFlips).compile()

def register(EntID):
	G.CONN.execute(
		C.FC.insert(), {
			"EntID": EntID,
			"FlipX": False,
			"FlipY": False,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.FC.select().where(C.FC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.FC	.delete()
			.where(C.FC.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.FC.c.FlipX, C.FC.c.FlipY]) \
			.select_from(C.FC) \
			.where(C.FC.c.EntID == EntID)
	).fetchone()

def store(EntID, FlipX, FlipY):
	G.CONN.execute(
		C.FC.update().where(
			C.FC.c.EntID == EntID
		), {
			"FlipX": FlipX,
			"FlipY": FlipY,
		}
	)

# TODO: Make this function obsolete by automatically registering images whenever an entity is registered
def registerImage(ImageID):
	noflipped = ImageID
	xflipped = R.IR.append(
		pg.transform.flip(R.IR[ImageID], True, False)
	)
	yflipped = R.IR.append(
		pg.transform.flip(R.IR[ImageID], False, True)
	)
	xyflipped = R.IR.append(
		pg.transform.flip(R.IR[ImageID], True, True)
	)
	
	G.CONN.execute(
		C.FI.insert(), [
			{"InImageID": ImageID, "FlipX": False,	"FlipY": False,	"OutImageID": ImageID},
			{"InImageID": ImageID, "FlipX": True,	"FlipY": False,	"OutImageID": xflipped},
			{"InImageID": ImageID, "FlipX": False,	"FlipY": True,	"OutImageID": yflipped},
			{"InImageID": ImageID, "FlipX": True,	"FlipY": True,	"OutImageID": xyflipped},
		]
	)
	
	G.CONN.execute(
		C.I.insert(), [
			# We assume 'ImageID' has already been registered
			{"ImageID": xflipped},
			{"ImageID": yflipped},
			{"ImageID": xyflipped},
		]
	)

def render():
	global renderQuery
	return G.CONN.execute(renderQuery).fetchall()
