#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G

# We don't have to keep track of the dirty regions assuming that 'ImageComp', 'DrawComp' and 'RectComp' aren't modified between the 'update' and 'clear' calls

drawQuery = None
RIPairsQuery = None
renderSteps = []
erased = []

from .. import Component as C
from .. import Resource as R

def init():
	global drawQuery, RIPairsQuery
	
	drawQuery = sqa.select([
		C.DC.c.ImageID,
		C.RECC.c.RectID,
	]).select_from(
		C.DC.join(C.RECC,
			C.DC.c.EntID == C.RECC.c.EntID,
		)
	).compile()
	
	RIPairsQuery = sqa.select([
		C.RECC.c.RectID,
		C.DC.c.ImageID,
	]).select_from(
		C.DC.join(C.RECC, C.DC.c.EntID == C.RECC.c.EntID)
	).compile()

def addRenderStep(step):
	global renderSteps
	renderSteps.append(step)

def _updateDrawComp(values):
	G.CONN.execute(C.DC.delete())			# Empty the drawing table
	if 0 < len(values):
		G.CONN.execute(C.DC.insert(), values)	# Repopulate the table with the given values (must be dict-like (have Key-Value pairs), such as a row proxy)

def _resetDrawComp():
	_updateDrawComp(G.CONN.execute(C.IC.select()).fetchall())

def _updateRects():
	global RIPairsQuery
	
	for RectID, ImageID in G.CONN.execute(RIPairsQuery).fetchall():
		R.RR[RectID] = R.IR[ImageID].get_rect()

def render():
	_resetDrawComp()
	
	global renderSteps
	for step in renderSteps:
		_updateDrawComp(step())
	
	_updateRects()

def update(screen):
	global drawQuery, erased
	
	newRects = []
	for ImageID, RectID in G.CONN.execute(drawQuery).fetchall():
		rect = R.RR[RectID]
		screen.blit(R.IR[ImageID], rect)
		newRects.append(rect)
	
	result = newRects + erased
	erased = []
	
	return result

def clear(screen, bgd):
	global erased
	
	for (RectID,) in G.CONN.execute(sqa.select([C.RECC.c.RectID]).select_from(C.RECC)).fetchall():
		screen.blit(bgd, R.RR[RectID])
		erased.append(R.RR[RectID].copy()) # The 'copy' part is important since the rectangle could be modified and not represent the region that needs to be erased upon the next draw
