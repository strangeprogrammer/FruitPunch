#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

import G
import Component
import Resource

# We don't have to keep track of the dirty regions assuming that 'ImageComp' and 'RectComp' aren't modified between the 'update' and 'clear' calls

@Resource.require("RectRes")
@Resource.require("ImageRes")
@Component.require("RectComp")
@Component.require("ImageComp")
def update(IC, RC, IR, RR, screen):
	drawables = G.CONN.execute(sqa.select([
		IC.c.ImageID,
		RC.c.RectID,
	]).select_from(
		IC.join(RC,
			IC.c.EntID == RC.c.EntID,
		)
	)).fetchall()
	
	for ImageID, RectID in drawables:
		screen.blit(IR[ImageID], RR[RectID])

@Resource.require("RectRes")
@Component.require("RectComp")
def clear(RC, RR, screen, bgd):
	for RectID in G.CONN.execute(RC.select(RC.c.RectID)).fetchall(): # Select only rectangle column
		screen.blit(bgd, RR[RectID])
