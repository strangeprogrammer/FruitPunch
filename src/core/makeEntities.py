#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD
import math

from . import Component as C
from . import Resource as R
from . import Entity
from . import G

from .Systems import Position
from .Systems import Velocity
from .Systems import Accel
from .Systems import Rotation
from .Systems import RotVel
from .Systems import Strut
from .Systems import Collision

def makeEntities():
	
	BYH = R.YCR.append(expelUp)
	BNH = 0
	
	makeAllEnt()
	makeRotVelStrut()
	makeGround(BYH, BNH)

FEntID = None

def makeAllEnt():
	FImage = LD("./RESOURCES/F.png").convert_alpha()
	FRect = FImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FImage, FRect, (200, 200))
	
	Velocity.register(EntID)
	Accel.register(EntID)
	Accel.set(0, 0, 0.4 / 1000)
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

def makeGround(BYH, BNH):
	BlueImage = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (200, 400))
	
	Collision.register(EntID)
	Collision.setState(EntID, BYH, BNH)

def expelUp(EntID, Ent2ID):
	RectID = G.CONN.execute(
		C.RECC.select().where(C.RECC.c.EntID == EntID)
	).fetchone()[1]
	
	Rect2ID = G.CONN.execute(
		C.RECC.select().where(C.RECC.c.EntID == Ent2ID)
	).fetchone()[1]
	
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.bottom = Rect1.top
	Position.set(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.get(Ent2ID)
	Velocity.set(Ent2ID, VelX, min(0, VelY))
