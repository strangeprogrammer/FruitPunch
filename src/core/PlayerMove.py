#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa
import math

from . import G
from . import Events

from .Systems import Velocity
from .Systems import RotVel
from .Systems import Camera

"""
Every time an important button is pressed, the flip state or rotation of all player-controlled entities is updated according to the key pressed.
"""

from . import Component as C

def init():
	Events.register(pg.KEYDOWN, keyDownHandler)
	Events.register(pg.KEYUP, keyUpHandler)

def keyDownHandler(e):
	if e.key in [
		pg.K_f,
		pg.K_d,
	]:
		rotHandler(e)
	elif e.key in [
		pg.K_UP,
		pg.K_DOWN,
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		moveHandler(e)
	elif e.key in [
		pg.K_i,
		pg.K_k,
		pg.K_j,
		pg.K_l,
	]:
		camHandler(e)

def keyUpHandler(e):
	if e.key in [
		pg.K_UP,
		pg.K_DOWN,
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		unMoveHandler(e)

def camHandler(e):
	EntID = Camera.EntID
	
	(VelX, VelY) = Velocity.get(EntID)
	
	if e.key == pg.K_i:
		Velocity.set(EntID, VelX, VelY + 0.5)
	elif e.key == pg.K_k:
		Velocity.set(EntID, VelX, VelY - 0.5)
	elif e.key == pg.K_j:
		Velocity.set(EntID, VelX + 0.5, VelY)
	elif e.key == pg.K_l:
		Velocity.set(EntID, VelX - 0.5, VelY)

def moveHandler(e):
	(dx, dy) = (0, 0)
	
	if e.key == pg.K_UP:
		dy -= 0.5
	elif e.key == pg.K_LEFT:
		dx -= 0.5
	elif e.key == pg.K_RIGHT:
		dx += 0.5
	
	for (player,) in G.CONN.execute(C.PLYC.select()).fetchall():
		if 0 < Velocity.instances(player):
			(VelX, VelY) = Velocity.get(player)
			Velocity.set(player, VelX + dx, VelY + dy)

def unMoveHandler(e):
	for (player,) in G.CONN.execute(C.PLYC.select()).fetchall():
		if 0 < Velocity.instances(player):
			(VelX, VelY) = Velocity.get(player)
			Velocity.set(player, 0, VelY)

def rotHandler(e):
	if e.key == pg.K_f:
		dOmega = -math.tau / 16 / 1000
	elif e.key == pg.K_d:
		dOmega = math.tau / 16 / 1000
	
	for (player,) in G.CONN.execute(C.PLYC.select()).fetchall():
		if 0 < RotVel.instances(player):
			RotVel.set(player, RotVel.get(player) + dOmega)
