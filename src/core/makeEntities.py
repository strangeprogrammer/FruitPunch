#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD
import math

from . import Component as C
from . import Resource as R
from . import Entity
from . import G

from .Systems import Velocity
from .Systems import Accel
from .Systems import Rotation
from .Systems import RotVel
from .Systems import Strut
from .Systems import Collision

BlueImage = GreenImage = YellowImage = BI = GI = YI = None

def makeEntities():
	global BlueImage, GreenImage, YellowImage, BI, GI, YI
	
	BYH = R.YCR.append(bumpYHandle)
	BNH = R.NCR.append(bumpNHandle)
	
	BlueImage = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	GreenImage = LD("./RESOURCES/GreenSquare.png").convert_alpha()
	YellowImage = LD("./RESOURCES/YellowSquare.png").convert_alpha()
	
	BI = R.IR.append(BlueImage)
	GI = R.IR.append(GreenImage)
	YI = R.IR.append(YellowImage)
	
	makeAllEnt()
	makeRotVelStrut()
	makeBump1(BYH, BNH, BlueImage)
	makeBump2(BYH, BNH, BlueImage)

FEntID = None

def makeAllEnt():
	FImage = LD("./RESOURCES/F.png").convert_alpha()
	FRect = FImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FImage, FRect, (200, 200))
	
	Accel.register(EntID)
	Velocity.register(EntID)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	Collision.register(EntID)
	
	global FEntID
	FEntID = EntID

def makeRotVelStrut():
	FiveImage = LD("./RESOURCES/5.png").convert_alpha()
	FiveRect = FiveImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(FiveImage, FiveRect, (400, 200))
	
	Rotation.register(EntID)
	RotVel.register(EntID)
	RotVel.set(EntID, math.tau / 32 / 1000)
	
	Collision.register(EntID)
	
	global FEntID
	Strut.register(FEntID, EntID)
	Strut.set(EntID, 200, 0)

numbumps = 0
bumpents = set()

def imageChooser():
	global BI, GI, YI, numbumps, bumpents
	
	if numbumps == 0:
		ImageID = BI
	elif numbumps == 1:
		ImageID = GI
	elif numbumps == 2:
		ImageID = YI
	
	for EntID in bumpents:
		G.CONN.execute(
			C.IC.update().where(C.IC.c.EntID == EntID), {
				"ImageID": ImageID,
			}
		)

def bumpYHandle(EntID, Ent2ID):
	global numbumps
	
	numbumps += 1
	
	imageChooser()

def bumpNHandle(EntID, Ent2ID):
	global numbumps
	
	numbumps -= 1
	
	imageChooser()

def makeBump1(BYH, BNH, BlueImage):
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (200, 400))
	
	Collision.register(EntID)
	Collision.setState(EntID, BYH, BNH)
	
	global bumpents
	bumpents.add(EntID)

def makeBump2(BYH, BNH, BlueImage):
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (400, 400))
	
	Collision.register(EntID)
	Collision.setState(EntID, BYH, BNH)
	
	global bumpents
	bumpents.add(EntID)
