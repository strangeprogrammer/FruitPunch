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



import Component
import Resource
import G

entCounter = None
rectCounter = None
imageCounter = None

def init():
	global entCounter, rectCounter, imageCounter
	from itertools import count
	entCounter = count()
	rectCounter = count()
	imageCounter = count()

@Resource.require("RectRes")
@Resource.require("ImageRes")
@Component.require("VelocityComp")
@Component.require("PositionComp")
@Component.require("RectComp")
@Component.require("ImageComp")
@Component.require("AllMove")
@Component.require("AllRects")
@Component.require("AllImages")
@Component.require("AllEnts")
def create(E, I, R, M, IC, RC, PC, VC, IR, RR, image, rect, center, velocity):
	rect.center = center
	
	global entCounter, rectCounter, imageCounter
	EntID = next(entCounter)
	RectID = next(rectCounter)
	ImageID = next(imageCounter)
	
	G.CONN.execute(E.insert().values(EntID = EntID))
	G.CONN.execute(I.insert().values(ImageID = ImageID))
	G.CONN.execute(R.insert().values(RectID = RectID))
	G.CONN.execute(M.insert().values(EntID = EntID))
	
	G.CONN.execute(IC.insert().values(EntID = EntID, ImageID = ImageID))
	G.CONN.execute(RC.insert().values(EntID = EntID, RectID = RectID))
	G.CONN.execute(PC.insert().values(RectID = RectID, PosX = center[0], PosY = center[1]))
	G.CONN.execute(VC.insert().values(RectID = RectID, VelX = velocity[0], VelY = velocity[1]))
	
	IR[ImageID] = image
	RR[RectID] = rect
	
	return EntID, RectID, ImageID

@Component.require("PlayerComp")
def createPlayer(PC, image, rect, center, velocity):
	EntID = create(image, rect, center, velocity)[0]
	G.CONN.execute(PC.insert().values(EntID = EntID))
