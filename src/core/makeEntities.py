#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from pygame.image import load as LD

from . import Entity
from . import G

def makeEntities():
	redImage = LD("./RESOURCES/RedSquare.png")
	redRect = redImage.get_rect()
	Entity.createPlayer(redImage, redRect, (200, 200), (0, 0))
