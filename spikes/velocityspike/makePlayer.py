#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

from physBodies.velocity import velocityBody

def makePlayer():
	return velocityBody(image = pg.image.load("../RESOURCES/0.png"), layer = 1, center = [500, 200])
