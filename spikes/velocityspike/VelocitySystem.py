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

movingQuery = None

@Component.require("VelocityComp")
@Component.require("PositionComp")
@Component.require("RectComp")
@Component.require("AllMove")
def init(M, RC, PC, VC):
	global movingQuery
	movingQuery = sqa.select([
		RC.c.RectID,
		PC.c.PosX,
		PC.c.PosY,
		VC.c.VelX,
		VC.c.VelY,
	]).select_from(
		M	.join(RC, M.c.EntID == RC.c.EntID) \
			.join(PC, RC.c.RectID == PC.c.RectID) \
			.join(VC, PC.c.RectID == VC.c.RectID)
	).compile()

@Resource.require("RectRes")
@Component.require("PositionComp")
def update(PC, RR, dt):
	global movingQuery
	for RectID, PosX, PosY, VelX, VelY in G.CONN.execute(movingQuery).fetchall():
		newX = PosX + VelX * dt
		newY = PosY + VelY * dt
		G.CONN.execute(
			PC.update().where(
				PC.c.RectID == RectID,
			).values(
				PosX = newX,
				PosY = newY,
			)
		)
		RR[RectID].center = (newX, newY)
