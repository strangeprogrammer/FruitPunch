#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from . import G
from . import Component
from . import Events

from .Systems import Velocity

"""
Every time an important button is pressed, the velocity of all player-controlled entities is updated according to the key pressed.
"""

def init():
	Events.register(pg.KEYDOWN, keyDownHandler)

def keyDownHandler(e):
	if e.key in [
		pg.K_UP,
		pg.K_DOWN,
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		moveHandler(e)

@Component.require("VelComp")
@Component.require("PlayerComp")
def moveHandler(PC, VC, e):
	(X, Y) = (0, 0)
	
	if e.key == pg.K_UP:
		Y -= 0.1
	elif e.key == pg.K_DOWN:
		Y += 0.1
	elif e.key == pg.K_LEFT:
		X -= 0.1
	elif e.key == pg.K_RIGHT:
		X += 0.1
	
	for (player,) in G.CONN.execute(PC.select()).fetchall():
		oldX, oldY = Velocity.get(player)
		Velocity.set(player, oldX + X, oldY + Y)
