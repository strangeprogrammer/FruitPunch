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

NoColl = EU = ED = EL = ER = None

def makeEntities():
	global NoColl, EU, ED, EL, ER
	
	NoColl = 0
	EU = R.CR.append(ejectUp)
	ED = R.CR.append(ejectDown)
	EL = R.CR.append(ejectLeft)
	ER = R.CR.append(ejectRight)
	
	makeAllEnt()
	makeRotVelStrut()
	makeTop()
	makeBottom()
	makeLeft()
	makeRight()

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
	
	global FEntID
	Strut.register(FEntID, EntID)
	Strut.set(EntID, 200, 0)

def makeTop():
	BlueImage = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (200, 200))
	
	global ED, NoColl
	Collision.register(EntID)
	Collision.setState(EntID, ED, ED, NoColl)

def makeBottom():
	BlueImage = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (200, 500))
	
	global EU, NoColl
	Collision.register(EntID)
	Collision.setState(EntID, EU, EU, NoColl)

def makeLeft():
	BlueImage = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (100, 400))
	
	global ER, NoColl
	Collision.register(EntID)
	Collision.setState(EntID, ER, ER, NoColl)

def makeRight():
	BlueImage = LD("./RESOURCES/BlueSquare.png").convert_alpha()
	BlueRect = BlueImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(BlueImage, BlueRect, (300, 400))
	
	global EL, NoColl
	Collision.register(EntID)
	Collision.setState(EntID, EL, EL, NoColl)

def ejectUp(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.bottom = Rect1.top
	Position.set(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.get(Ent2ID)
	Velocity.set(Ent2ID, VelX, min(0, VelY))

def ejectDown(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.top = Rect1.bottom
	Position.set(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.get(Ent2ID)
	Velocity.set(Ent2ID, VelX, max(0, VelY))

def ejectLeft(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.right = Rect1.left
	Position.set(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.get(Ent2ID)
	Velocity.set(Ent2ID, min(0, VelX), VelY)

def ejectRight(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.left = Rect1.right
	Position.set(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.get(Ent2ID)
	Velocity.set(Ent2ID, max(0, VelX), VelY)
