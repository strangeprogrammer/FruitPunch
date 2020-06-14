#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G
from .. import Component
from ..Component import require as require
from .. import Resource

# We don't have to keep track of the dirty regions assuming that 'ImageComp', 'DrawComp' and 'RectComp' aren't modified between the 'update' and 'clear' calls

drawQuery = None
renderSteps = []

@require("RectComp")
@require("DrawComp")
def init(DC, RC):
	G.SCREEN = pg.display.set_mode()
	G.SCREEN.fill( (255, 255, 255) )
	
	G.BGD = G.SCREEN.copy()
	pg.display.flip()
	
	global drawQuery
	drawQuery = sqa.select([
		DC.c.ImageID,
		RC.c.RectID,
	]).select_from(
		DC.join(RC,
			DC.c.EntID == RC.c.EntID,
		)
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

def render():
	_resetDrawComp()
	global renderSteps
	for step in renderSteps:
		_updateDrawComp(step())

@Resource.require("RectRes")
@Resource.require("ImageRes")
def update(IR, RR, screen):
	global drawQuery
	
	result = []
	for ImageID, RectID in G.CONN.execute(drawQuery).fetchall():
		rect = RR[RectID]
		screen.blit(IR[ImageID], rect)
		result.append(rect)
	
	return result

@Resource.require("RectRes")
@require("AllRects")
def clear(R, RR, screen, bgd):
	for (RectID, ) in G.CONN.execute(sqa.select([R.c.RectID]).select_from(R)).fetchall():
		screen.blit(bgd, RR[RectID])
