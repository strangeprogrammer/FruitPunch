#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD
import math

from . import Entity
from . import G

from .Systems import Velocity
from .Systems import Flip
from .Systems import Rotation
from .Systems import FlipDoll
from .Systems import RotDoll

FEntID = None

def makeEntities():
	makeAllEnt()
	makeFlipDoll()
	makeRotDoll()
	makeNone()

def makeAllEnt():
	FImage = LD("./RESOURCES/F.png")
	FRect = FImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FImage, FRect, (200, 200))
	
	Flip.register(EntID)
	Flip.registerImage(ImageID)
	Velocity.register(EntID)
	Rotation.register(EntID)
	
	global FEntID
	FEntID = EntID

def makeFlipDoll():
	FiveImage = LD("./RESOURCES/5.png")
	FiveRect = FiveImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(FiveImage, FiveRect, (400, 200))
	
	Flip.register(EntID)
	Flip.registerImage(ImageID)
	
	global FEntID
	FlipDoll.register(FEntID, EntID)
	FlipDoll.set(EntID, True, True)

def makeRotDoll():
	TwoImage = LD("./RESOURCES/2.png")
	TwoRect = TwoImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(TwoImage, TwoRect, (200, 400))
	
	Rotation.register(EntID)
	
	global FEntID
	RotDoll.register(FEntID, EntID)
	RotDoll.set(EntID, math.tau / 4)

def makeNone():
	NoneImage = LD("./RESOURCES/7.png")
	NoneRect = NoneImage.get_rect()
	
	Entity.create(NoneImage, NoneRect, (400, 400))
