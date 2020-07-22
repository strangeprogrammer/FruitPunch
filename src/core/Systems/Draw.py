#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G
from ..Misc import Rect

drawQuery = None
RIPairsQuery = None
renderSteps = []

from .. import Component as C
from .. import Resource as R

from . import Camera

bgd = None

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

def quit():
	G.CONN.execute(
		C.DC.delete()
	)
	
	global renderSteps
	renderSteps = []
	
	global bgd
	bgd = None

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
		oldrect = R.RR[RectID]
		newrect = Rect(R.IR[ImageID].get_rect())
		newrect.center = oldrect.center
		R.RR[RectID] = newrect # XXX WARNING: this will replace any rectangle that the original image was associated with while preserving the center
	
	R.RR.flush()

def render():
	_resetDrawComp()
	
	global renderSteps
	for step in renderSteps:
		_updateDrawComp(step())
	
	_updateRects()

def _blackPad(bgd, camRect):
	badlands = Rect(bgd.get_rect()).cleanCrack(camRect)
	badlands = list(map(lambda r: r - camRect, badlands))
	outsurfaces = list(map(lambda r: G.SCREEN.subsurface(r), badlands))
	
	for s in outsurfaces:
		s.fill([0, 0, 0])

def update():
	global bgd, drawQuery
	
	camRect = R.RR[Camera.RectID]
	
	# Draw the background first
	G.SCREEN.blit(bgd, (0, 0), camRect)
	_blackPad(bgd, camRect)
	
	# Draw all entities
	for ImageID, RectID in G.CONN.execute(drawQuery).fetchall():
		rect = R.RR[RectID]
		if rect.colliderect(camRect):
			G.SCREEN.blit(
				R.IR[ImageID],
				rect - camRect,
				Rect(0, 0, rect.width, rect.height)
			)
	
	pg.display.flip()
