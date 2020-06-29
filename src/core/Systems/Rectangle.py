#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .. import G

from .. import Component as C

def register(EntID):
	G.CONN.execute(
		C.RECC.insert(), {
			"EntID": EntID,
			"RectID": -1,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.RECC.select().where(C.RECC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.RECC.delete().where(C.RECC.c.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.RECC.c.RectID]) \
			.select_from(C.RECC) \
			.where(C.RECC.c.EntID == EntID)
	).fetchone()[0]

def store(EntID, RectID):
	G.CONN.execute(
		C.RECC	.update() \
			.where(C.RECC.c.EntID == EntID), {
			"RectID": RectID,
		}
	)
