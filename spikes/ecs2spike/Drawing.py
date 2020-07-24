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
