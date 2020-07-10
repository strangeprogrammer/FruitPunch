#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G

from .. import Component as C

def register(EntID):
	G.CONN.execute(
		C.IC.insert(), {
			"EntID": EntID,
			"ImageID": -1,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.IC.select().where(C.IC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.IC.delete().where(C.IC.c.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.IC.c.ImageID]) \
			.select_from(C.IC) \
			.where(C.IC.c.EntID == EntID)
	).fetchone()[0]

def store(EntID, ImageID):
	G.CONN.execute(
		C.IC	.update() \
			.where(C.IC.c.EntID == EntID), {
			"ImageID": ImageID,
		}
	)
