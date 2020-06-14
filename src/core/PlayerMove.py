#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa
import math

from . import G
from . import Component
from .Component import require
from . import Events

from .Systems import Velocity
from .Systems import Flip
from .Systems import Rotation

"""
Every time an important button is pressed, the flip state or rotation of all player-controlled entities is updated according to the key pressed.
"""

def init():
	Events.register(pg.KEYDOWN, keyDownHandler)

def keyDownHandler(e):
	if e.key in [
		pg.K_a,
		pg.K_s,
	]:
		rotationHandler(e)
	elif e.key in [
		pg.K_f,
		pg.K_d,
	]:
		flipHandler(e)

@require("VelComp")
@require("PlayerComp")
def rotationHandler(PC, VC, e):
	Theta = 0
	
	if e.key == pg.K_a:
		Theta += math.tau / 64
	elif e.key == pg.K_s:
		Theta -= math.tau / 64
	
	for (player,) in G.CONN.execute(PC.select()).fetchall():
		if 0 < Rotation.instances(player):
			Rotation.set(player, Rotation.get(player) + Theta)

@require("FlipComp")
@require("PlayerComp")
def flipHandler(PC, FC, e):
	for (player,) in G.CONN.execute(PC.select()).fetchall():
		if 0 < Flip.instances(player):
			FlipX, FlipY = Flip.get(player)
			
			if e.key == pg.K_f:
				FlipX = not FlipX
			elif e.key == pg.K_d:
				FlipY = not FlipY
			
			Flip.set(player, FlipX, FlipY)
