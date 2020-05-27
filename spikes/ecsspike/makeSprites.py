#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import math

import pygame as pg
from pygame import sprite as PGS
from pygame.image import load as LD

def scaleAnimation(sprite, time):
	scale = math.sin(time / 1000) * 0.25 + 1 # Segfault when scale becomes 0, so we can't allow that
	newWidth = int(scale * sprite.origRect.width)
	newHeight = int(scale * sprite.origRect.height)
	sprite.image = pg.transform.smoothscale(sprite.image, (newWidth, newHeight))

scaleAnimation.centerPreserving = True
scaleAnimation.rectGenerating = True

def twistAnimation(sprite, time):
	angleMax = (360 / math.tau) * (math.pi / 4)
	angle = math.sin(time / 1000) * angleMax
	sprite.image = pg.transform.rotate(sprite.image, angle)

twistAnimation.centerPreserving = True
twistAnimation.rectGenerating = True

def makeBox(path, center):
	sprite = PGS.Sprite()
	sprite.origImage = LD(path)
	sprite.rect = sprite.origImage.get_rect()
	sprite.origRect = sprite.rect.copy()
	sprite.rect.center = center
	sprite.contAnimations = [scaleAnimation, twistAnimation]
	
	return sprite

def makeSprites():
	a = makeBox("../RESOURCES/RedSquare.png", (300, 300))
	b = makeBox("../RESOURCES/BlueSquare.png", (500, 300))
	c = makeBox("../RESOURCES/GreenSquare.png", (700, 300))
	d = makeBox("../RESOURCES/YellowSquare.png", (900, 300))
	
	return PGS.Group(a, b, c, d)
