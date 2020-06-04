#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

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
