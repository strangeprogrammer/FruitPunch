#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa
import math

from . import G
from . import Events

from .Systems import Velocity
from .Systems import RotVel
from .Systems import Flip

from . import Component as C

def init():
	Events.register(pg.KEYDOWN, keyDownHandler)
	Events.register(pg.KEYUP, keyUpHandler)

def quit():
	Events.deregister(pg.KEYDOWN)
	Events.deregister(pg.KEYUP)

def keyDownHandler(e):
	if e.key in [
		pg.K_f,
		pg.K_d,
	]:
		rotHandler(e)
	elif e.key in [
		pg.K_UP,
	]:
		moveHandler(e)
	elif e.key in [
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		moveHandler(e)
		flipHandler(e)

def keyUpHandler(e):
	if e.key in [
		pg.K_UP,
		pg.K_DOWN,
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		unMoveHandler(e)

def moveHandler(e):
	(dx, dy) = (0, 0)
	
	if e.key == pg.K_UP:
		dy -= 0.5
	elif e.key == pg.K_LEFT:
		dx -= 0.5
	elif e.key == pg.K_RIGHT:
		dx += 0.5
	
	for [player] in G.CONN.execute(C.PLYC.select()).fetchall():
		if 0 < Velocity.instances(player):
			(VelX, VelY) = Velocity.fetch(player)
			Velocity.store(player, VelX + dx, VelY + dy)

def flipHandler(e):
	for [player] in G.CONN.execute(C.PLYC.select()).fetchall():
		[FlipX, FlipY] = Flip.fetch(player)
		Flip.store(player, e.key == pg.K_LEFT, FlipY)

def unMoveHandler(e):
	if e.key in [
		pg.K_LEFT,
		pg.K_RIGHT,
	]:
		for [player] in G.CONN.execute(C.PLYC.select()).fetchall():
			if 0 < Velocity.instances(player):
				(VelX, VelY) = Velocity.fetch(player)
				Velocity.store(player, 0, VelY)

def rotHandler(e):
	if e.key == pg.K_f:
		dOmega = -math.tau / 16 / 1000
	elif e.key == pg.K_d:
		dOmega = math.tau / 16 / 1000
	
	for [player] in G.CONN.execute(C.PLYC.select()).fetchall():
		if 0 < RotVel.instances(player):
			RotVel.store(player, RotVel.fetch(player) + dOmega)
