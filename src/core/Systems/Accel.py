#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G
from .. import Time

from .. import Component as C

from . import Velocity

movingQuery = None

def init():
	global movingQuery
	
	movingQuery = sqa.select([
		C.AC.c.EntID,
		C.AC.c.AccX,
		C.AC.c.AccY,
	]).select_from(
		C.AC,
	).compile()

def quit():
	G.CONN.execute(
		C.AC.delete()
	)

def register(EntID):
	G.CONN.execute(
		C.AC.insert(), {
			"EntID": EntID,
			"AccX": 0,
			"AccY": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.AC.select().where(C.AC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.AC.delete().where(C.AC.c.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.AC.c.AccX, C.AC.c.AccY]) \
			.select_from(C.AC) \
			.where(C.AC.c.EntID == EntID)
	).fetchone()

def store(EntID, AccX, AccY):
	G.CONN.execute(
		C.AC	.update() \
			.where(C.AC.c.EntID == EntID), {
			"AccX": AccX,
			"AccY": AccY,
		}
	)

def update():
	global movingQuery
	
	for EntID, AccX, AccY in G.CONN.execute(movingQuery).fetchall():
		(VelX, VelY) = Velocity.fetch(EntID)
		newX = VelX + AccX * Time.elapsed
		newY = VelY + AccY * Time.elapsed
		Velocity.store(EntID, newX, newY)
