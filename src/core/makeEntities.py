#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD

from . import Entity
from . import G

from .Systems import Flip
from .Systems import Rotation

def makeEntities():
	makeFlipRot()
	makeRot()
	makeFlip()
	makeNone()

def makeFlipRot():
	FImage = LD("./RESOURCES/F.png")
	FRect = FImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FImage, FRect, (200, 200))
	
	Flip.register(EntID)
	Flip.registerImage(ImageID)
	
	Rotation.register(EntID)

def makeRot():
	TwoImage = LD("./RESOURCES/2.png")
	TwoRect = TwoImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(TwoImage, TwoRect, (400, 200))
	
	Rotation.register(EntID)

def makeFlip():
	FiveImage = LD("./RESOURCES/5.png")
	FiveRect = FiveImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(FiveImage, FiveRect, (200, 400))
	
	Flip.register(EntID)
	Flip.registerImage(ImageID)

def makeNone():
	NoneImage = LD("./RESOURCES/7.png")
	NoneRect = NoneImage.get_rect()
	
	EntID, ImageID, RectID = Entity.createPlayer(NoneImage, NoneRect, (400, 400))
