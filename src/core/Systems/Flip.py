#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

# Copyright (C) 2020 Stephen Fedele <32551324+strangeprogrammer@users.noreply.github.com>
# 
# This file is part of Fruit Punch.
# 
# Fruit Punch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Fruit Punch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Fruit Punch.  If not, see <https://www.gnu.org/licenses/>.
# 
# Additional terms apply to this file.  Read the file 'LICENSE.txt' for
# more information.



import pygame as pg
import sqlalchemy as sqa

from .. import G

renderQuery = None

from .. import Component as C
from .. import Resource as R

def init():
	global renderQuery
	
	exempt = sqa.select([
		C.DC.c.EntID,
		C.DC.c.ImageID,
	]).select_from(
		C.DC
	).where(
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

def quit():
	G.CONN.execute(
		C.FC.delete()
	)
	
	flippedImages = G.CONN.execute(
		sqa.select([
			C.FI.c.OutImageID
		]).select_from(
			C.FI
		).where(
			C.FI.c.FlipX == sqa.literal(True) |
			C.FI.c.FlipY == sqa.literal(True)
		)
	).fetchall()
	
	for [ImageID] in flippedImages:
		del R.IR[ImageID]
	
	R.IR.flush()
	
	G.CONN.execute(
		C.FI.delete()
	)

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
		C.FC.select(C.FC.c.EntID == EntID)
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
	
	R.IR.flush()
	
	G.CONN.execute(
		C.FI.insert(), [
			{"InImageID": ImageID, "FlipX": False,	"FlipY": False,	"OutImageID": ImageID},
			{"InImageID": ImageID, "FlipX": True,	"FlipY": False,	"OutImageID": xflipped},
			{"InImageID": ImageID, "FlipX": False,	"FlipY": True,	"OutImageID": yflipped},
			{"InImageID": ImageID, "FlipX": True,	"FlipY": True,	"OutImageID": xyflipped},
		]
	)

def render():
	global renderQuery
	return G.CONN.execute(renderQuery).fetchall()
