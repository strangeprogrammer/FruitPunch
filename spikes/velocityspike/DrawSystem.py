#!/bin/sed -e 3q;d

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
