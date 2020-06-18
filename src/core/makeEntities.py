#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD
import math

from . import Entity
from . import G

from .Systems import Velocity
from .Systems import Rotation
from .Systems import RotVel
from .Systems import Strut

def makeEntities():
	makeAllEnt()
	makeRotVelStrut()
	makeRotVel()
	makeNone()

global FEntID

def makeAllEnt():
	FImage = LD("./RESOURCES/F.png")
	FRect = FImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FImage, FRect, (200, 200))
	
	Velocity.register(EntID)
	Rotation.register(EntID)
	RotVel.register(EntID)
	
	global FEntID
	FEntID = EntID

def makeRotVelStrut():
	FiveImage = LD("./RESOURCES/5.png")
	FiveRect = FiveImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(FiveImage, FiveRect, (400, 200))
	
	Velocity.register(EntID)
	
	Rotation.register(EntID)
	RotVel.register(EntID)
	RotVel.set(EntID, math.tau / 32 / 1000)
	
	global FEntID
	Strut.register(FEntID, EntID)
	Strut.set(EntID, 200, 0)

def makeRotVel():
	TwoImage = LD("./RESOURCES/2.png")
	TwoRect = TwoImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(TwoImage, TwoRect, (200, 400))
	
	Rotation.register(EntID)
	RotVel.register(EntID)

def makeNone():
	NoneImage = LD("./RESOURCES/7.png")
	NoneRect = NoneImage.get_rect()
	
	Entity.createPlayer(NoneImage, NoneRect, (400, 400))
