#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G

drawQuery = None
RIPairsQuery = None
renderSteps = []
borderWidth = 0

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

def _drawBorder(scene):
	global borderWidth
	if 0 < borderWidth:
		origRect = scene.get_rect()
		rect = origRect.copy()
		rect.height -= borderWidth
		rect.width -= borderWidth
		rect.center = origRect.center
		pg.draw.rect(scene, (255, 0, 255), rect, borderWidth)

def update(scene, camRect):
	global drawQuery
	
	result = []
	for ImageID, RectID in G.CONN.execute(drawQuery).fetchall():
		rect = R.RR[RectID]
		if rect.colliderect(camRect):
			scene.blit(R.IR[ImageID], rect)
			result.append(rect)
	
	_drawBorder(scene)
	
	return result

def clear(scene, bgd, camRect):
	for (RectID,) in G.CONN.execute(sqa.select([C.RECC.c.RectID]).select_from(C.RECC)).fetchall():
		rect = R.RR[RectID]
		if rect.colliderect(camRect):
			scene.blit(bgd, rect, rect)
