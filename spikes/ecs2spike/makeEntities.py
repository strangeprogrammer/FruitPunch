#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pickle
from pygame.image import load as LD

import Component
import Resource
import G

@Resource.require("RectRes")
@Resource.require("ImageRes")
@Component.require("RectComp")
@Component.require("ImageComp")
@Component.require("AllEntities")
def makeEntities(E, IC, RC, IR, RR):
	redID = 0
	
	G.CONN.execute(E.insert().values(EntID = redID))
	G.CONN.execute(IC.insert().values(EntID = redID, ImageID = redID))
	G.CONN.execute(RC.insert().values(EntID = redID, RectID = redID))
	
	redImage = LD("../RESOURCES/RedSquare.png")
	redRect = redImage.get_rect()
	redRect.center = (200, 200)
	
	IR[redID] = redImage
	RR[redID] = redRect
