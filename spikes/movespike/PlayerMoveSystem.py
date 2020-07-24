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
import Events
import Resource

MOV = [0, 0]

def moveHandler(e):
	global MOV
	if e.key == pg.K_UP:
		MOV[1] -= 5
	elif e.key == pg.K_DOWN:
		MOV[1] += 5
	elif e.key == pg.K_LEFT:
		MOV[0] -= 5
	elif e.key == pg.K_RIGHT:
		MOV[0] += 5

def init():
	Events.register(pg.KEYDOWN, moveHandler)

@Resource.require("RectRes")
@Component.require("RectCenterComp")
@Component.require("RectComp")
@Component.require("PlayerComp")
def update(PC, RC, RCC, RR):
	moveRects = G.CONN.execute(sqa.select([
		RCC.c.RectID,
		RCC.c.CenterX,
		RCC.c.CenterY,
	]).select_from(
		PC.join(
			RC.join(
				RCC,
				RC.c.RectID == RCC.c.RectID,
			),
			PC.c.EntID == RC.c.EntID,
		)
	)).fetchall()
	
	global MOV
	
	for RectID, X, Y in moveRects:
		X += MOV[0]
		Y += MOV[1]
		RR[RectID].center = (X, Y)
		G.CONN.execute(RCC.update().where(
			RCC.c.RectID == RectID,
		).values(
			CenterX = X,
			CenterY = Y,
		))
	
	MOV = [0, 0]
