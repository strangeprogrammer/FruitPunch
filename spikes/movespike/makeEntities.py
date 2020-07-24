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



from pygame.image import load as LD

import Component
import Resource
import G

@Resource.require("RectRes")
@Resource.require("ImageRes")
@Component.require("PlayerComp")
@Component.require("RectCenterComp")
@Component.require("RectComp")
@Component.require("ImageComp")
@Component.require("AllRects")
@Component.require("AllImages")
@Component.require("AllEnts")
def makeEntities(E, I, R, IC, RC, RCC, PC, IR, RR):
	redID = 0
	
	redImage = LD("../RESOURCES/RedSquare.png")
	redRect = redImage.get_rect()
	redRect.center = (200, 200)
	
	G.CONN.execute(E.insert().values(EntID = redID))
	G.CONN.execute(I.insert().values(ImageID = redID))
	G.CONN.execute(R.insert().values(RectID = redID))
	
	G.CONN.execute(IC.insert().values(EntID = redID, ImageID = redID))
	G.CONN.execute(RC.insert().values(EntID = redID, RectID = redID))
	G.CONN.execute(RCC.insert().values(RectID = redID, CenterX = redRect.center[0], CenterY = redRect.center[1]))
	G.CONN.execute(PC.insert().values(EntID = redID))
	
	IR[redID] = redImage
	RR[redID] = redRect
