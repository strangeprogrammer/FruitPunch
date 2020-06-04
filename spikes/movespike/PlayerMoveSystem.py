#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

import G
import Component
import Events
import Resource

MOV = [0, 0]

def moveHandler(e):
	global MOV
	if e.key == pg.K_UP:
		MOV[1] -= 5
	elif e.key == pg.K_DOWN:
		MOV[1] += 5
	elif e.key == pg.K_LEFT:
		MOV[0] -= 5
	elif e.key == pg.K_RIGHT:
		MOV[0] += 5

def init():
	Events.register(pg.KEYDOWN, moveHandler)

@Resource.require("RectRes")
@Component.require("RectCenterComp")
@Component.require("RectComp")
@Component.require("PlayerComp")
def update(PC, RC, RCC, RR):
	moveRects = G.CONN.execute(sqa.select([
		RCC.c.RectID,
		RCC.c.CenterX,
		RCC.c.CenterY,
	]).select_from(
		PC.join(
			RC.join(
				RCC,
				RC.c.RectID == RCC.c.RectID,
			),
			PC.c.EntID == RC.c.EntID,
		)
	)).fetchall()
	
	global MOV
	
	for RectID, X, Y in moveRects:
		X += MOV[0]
		Y += MOV[1]
		RR[RectID].center = (X, Y)
		G.CONN.execute(RCC.update().where(
			RCC.c.RectID == RectID,
		).values(
			CenterX = X,
			CenterY = Y,
		))
	
	MOV = [0, 0]
