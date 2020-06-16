#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD

from . import Entity
from . import G

from .Systems import Velocity
from .Systems import Flip
from .Systems import FlipDoll

FEntID = None

def makeEntities():
	makeVelFlip()
	makeFlipDoll()
	makeNone()

def makeVelFlip():
	FImage = LD("./RESOURCES/F.png")
	FRect = FImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FImage, FRect, (200, 200))
	
	Flip.register(EntID)
	Flip.registerImage(ImageID)
	
	Velocity.register(EntID)
	
	global FEntID
	FEntID = EntID

def makeFlipDoll():
	FiveImage = LD("./RESOURCES/5.png")
	FiveRect = FiveImage.get_rect()
	
	EntID, ImageID, RectID = Entity.create(FiveImage, FiveRect, (200, 400))
	
	Flip.register(EntID)
	Flip.registerImage(ImageID)
	
	global FEntID
	FlipDoll.register(FEntID, EntID)
	FlipDoll.set(EntID, True, True)

def makeNone():
	NoneImage = LD("./RESOURCES/7.png")
	NoneRect = NoneImage.get_rect()
	
	Entity.create(NoneImage, NoneRect, (400, 400))
