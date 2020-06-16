#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg
import sqlalchemy as sqa

from .. import G
from .. import Component
from ..Component import require as require
from .. import Resource

toDollQuery = None

@require("FlipDollComp")
@require("FlipComp")
def init(FC, FDC):
	global toDollQuery
	
	toDollQuery = sqa.select([
		FDC.c.ChildID,
		FC.c.FlipX,
		FC.c.FlipY,
		FDC.c.OffX,
		FDC.c.OffY,
	]).select_from(
		FC.join(FDC, FC.c.EntID == FDC.c.EntID)
	).compile()

@require("FlipDollComp")
def register(FDC, EntID, ChildID):
	# Find out whether or not the entity being registered is in a chain of dolls, and assign to it its generation number as appropriate
	# The entity being registered should already be registered with the Flip System
#	try:
#		Generation = G.CONN.execute(
#			sqa.select([
#				FDC.c.Generation
#			]).select_from(FDC).where(
#				FDC.c.ChildID == EntID
#			)
#		).fetchone()[0]
#	except Exception:
#		Generation = 0
	
	G.CONN.execute(
		FDC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
#			"Generation": Generation,
			"OffX": False,
			"OffY": False,
		}
	)

@require("FlipDollComp")
def instances(FDC, ChildID):
	return len(G.CONN.execute(
		FDC.select().where(FDC.c.ChildID == ChildID)
	).fetchall())

@require("FlipDollComp")
def deregister(FDC, ChildID):
	G.CONN.execute(
		FDC.delete().where(FDC.c.ChildID == ChildID)
	)

@require("FlipDollComp")
def get(FDC, ChildID):
	return G.CONN.execute(
		sqa.select([
			FDC.c.OffX,
			FDC.c.OffY,
		]).select_from(FDC).where(
			FDC.c.ChildID == ChildID
		)
	).fetchone()

@require("FlipDollComp")
def set(FDC, ChildID, OffX, OffY):
	G.CONN.execute(
		FDC.update().where(FDC.c.ChildID == ChildID), {
			"OffX": OffX,
			"OffY": OffY,
		}
	)

@require("FlipComp")
def update(FC):
	# TODO: Implement update in phases based upon generation number
	for ChildID, FlipX, FlipY, OffX, OffY in G.CONN.execute(toDollQuery).fetchall():
		G.CONN.execute(
			FC.update().where(FC.c.EntID == ChildID),
			{
				"FlipX": bool(FlipX) ^ bool(OffX),
				"FlipY": bool(FlipY) ^ bool(OffY),
			}
		)
