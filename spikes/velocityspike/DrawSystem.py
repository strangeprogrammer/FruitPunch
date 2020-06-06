#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

import G
import Component
import Resource

# We don't have to keep track of the dirty regions assuming that 'ImageComp' and 'RectComp' aren't modified between the 'update' and 'clear' calls

drawQuery = None

@Component.require("RectComp")
@Component.require("ImageComp")
def init(IC, RC):
	G.SCREEN = pg.display.set_mode()
	G.SCREEN.fill( (255, 255, 255) )
	
	G.BGD = G.SCREEN.copy()
	pg.display.flip()
	
	global drawQuery
	drawQuery = sqa.select([
		IC.c.ImageID,
		RC.c.RectID,
	]).select_from(
		IC.join(RC,
			IC.c.EntID == RC.c.EntID,
		)
	).compile()

@Resource.require("RectRes")
@Resource.require("ImageRes")
def update(IR, RR, screen):
	global drawQuery
	drawables = G.CONN.execute(drawQuery).fetchall()
	
	result = []
	for ImageID, RectID in drawables:
		rect = RR[RectID]
		screen.blit(IR[ImageID], rect)
		result.append(rect)
	
	return result

@Resource.require("RectRes")
@Component.require("AllRects")
def clear(R, RR, screen, bgd):
	for (RectID, ) in G.CONN.execute(sqa.select([R.c.RectID]).select_from(R)).fetchall():
		screen.blit(bgd, RR[RectID], RR[RectID])
