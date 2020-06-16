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
		pg.K_f,
		pg.K_d,
	]:
		flipHandler(e)
	elif e.key in [
		pg.K_UP,
		pg.K_DOWN,
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		moveHandler(e)
	elif e.key in [
		pg.K_s,
		pg.K_a,
	]:
		rotHandler(e)

@require("PlayerComp")
def flipHandler(PC, e):
	for (player,) in G.CONN.execute(PC.select()).fetchall():
		if 0 < Flip.instances(player):
			FlipX, FlipY = Flip.get(player)
			
			if e.key == pg.K_f:
				FlipX = not FlipX
			elif e.key == pg.K_d:
				FlipY = not FlipY
			
			Flip.set(player, FlipX, FlipY)

@require("PlayerComp")
def moveHandler(PC, e):
	(dx, dy) = (0, 0)
	
	if e.key == pg.K_UP:
		dy -= 0.2
	elif e.key == pg.K_DOWN:
		dy += 0.2
	elif e.key == pg.K_LEFT:
		dx -= 0.2
	elif e.key == pg.K_RIGHT:
		dx += 0.2
	
	for (player,) in G.CONN.execute(PC.select()).fetchall():
		(VelX, VelY) = Velocity.get(player)
		Velocity.set(player, VelX + dx, VelY + dy)

@require("PlayerComp")
def rotHandler(PC, e):
	if e.key == pg.K_s:
		dTheta = -math.tau / 64
	elif e.key == pg.K_a:
		dTheta = math.tau / 64
	
	for (player,) in G.CONN.execute(PC.select()).fetchall():
		Theta = Rotation.get(player)
		Rotation.set(player, Theta + dTheta)
