#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G
from ..Component import require as require
from .. import Resource

# We don't have to keep track of the dirty regions assuming that 'ImageComp', 'DrawComp' and 'RectComp' aren't modified between the 'update' and 'clear' calls

drawQuery = None
RIPairsQuery = None
renderSteps = []
erased = []

@require("PosComp")
@require("RectComp")
@require("DrawComp")
def init(DC, RC, PC):
	G.SCREEN = pg.display.set_mode()
	G.SCREEN.fill( (255, 255, 255) )
	
	G.BGD = G.SCREEN.copy()
	pg.display.flip()
	
	global drawQuery, RIPairsQuery
	
	drawQuery = sqa.select([
		DC.c.ImageID,
		RC.c.RectID,
	]).select_from(
		DC.join(RC,
			DC.c.EntID == RC.c.EntID,
		)
	).compile()
	
	RIPairsQuery = sqa.select([
		RC.c.RectID,
		DC.c.ImageID,
		PC.c.PosX,
		PC.c.PosY,
	]).select_from(
		DC	.join(RC, DC.c.EntID == RC.c.EntID) \
			.join(PC, DC.c.EntID == PC.c.EntID)
	).compile()

def addRenderStep(step):
	global renderSteps
	renderSteps.append(step)

@require("DrawComp")
def _updateDrawComp(DC, values):
	G.CONN.execute(DC.delete())		# Empty the drawing table
	G.CONN.execute(DC.insert(), values)	# Repopulate the table with the given values (must be dict-like (have Key-Value pairs), such as a row proxy)

@require("ImageComp")
def _resetDrawComp(IC):
	_updateDrawComp(G.CONN.execute(IC.select()).fetchall())

@Resource.require("RectRes")
@Resource.require("ImageRes")
def _updateRects(IR, RR):
	global RIPairsQuery
	
	for RectID, ImageID, PosX, PosY in G.CONN.execute(RIPairsQuery).fetchall():
		RR[RectID] = IR[ImageID].get_rect()
		RR[RectID].center = (PosX, PosY)

def render():
	_resetDrawComp()
	
	global renderSteps
	for step in renderSteps:
		_updateDrawComp(step())
	
	_updateRects()

@Resource.require("RectRes")
@Resource.require("ImageRes")
def update(IR, RR, screen):
	global drawQuery, erased
	
	newRects = []
	for ImageID, RectID in G.CONN.execute(drawQuery).fetchall():
		rect = RR[RectID]
		screen.blit(IR[ImageID], rect)
		newRects.append(rect)
	
	result = newRects + erased
	erased = []
	
	return result

@Resource.require("RectRes")
@require("RectComp")
def clear(RC, RR, screen, bgd):
	global erased
	
	for (RectID,) in G.CONN.execute(sqa.select([RC.c.RectID]).select_from(RC)).fetchall():
		screen.blit(bgd, RR[RectID])
		erased.append(RR[RectID].copy()) # The 'copy' part is important since the rectangle could be modified and not represent the region that needs to be erased upon the next draw
