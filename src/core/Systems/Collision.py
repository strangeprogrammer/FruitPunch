#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from .. import G

from .. import Component as C
from .. import Resource as R

"""
This module currently uses an O(n^2) (brute-force) method of collision detection, and should be swapped out for something better in the future.
NOTE: Do NOT change the collision handler's index number while a collision is active (changing the handle itself is probably a bad idea, too).
"""

collQuery = None
prevCollisions = set()

def init():
	R.CR[0] = lambda E1, E2, R1, R2: None	# Default collision handler does nothing
	next(R.CR.counter)			# Adjust resource index so we don't accidentally overwrite default handler
	
	global collQuery
	
	RECC2 = C.RECC.alias()
	t1 = C.CT.join(C.RECC, C.CT.c.EntID == C.RECC.c.EntID)
	t2 = C.CU.join(RECC2, C.CU.c.EntID == RECC2.c.EntID)
	
	collQuery = sqa.select([
		C.CT.c.EntID,
		C.CU.c.EntID,
		C.RECC.c.RectID,
		RECC2.c.RectID,
		C.CT.c.OnColl,
		C.CT.c.OffColl,
	]).select_from(
		t1.join(t2, sqa.literal(True))
	).where(
		C.CT.c.EntID != C.CU.c.EntID # Objects can't collide with themselves (or at least, it makes programming simpler)
	).compile()

def quit():
	G.CONN.execute(
		C.CT.delete()
	)
	G.CONN.execute(
		C.CU.delete()
	)
	
	global prevCollisions
	prevCollisions = set()

def registerT(EntID, OnColl, OffColl):
	G.CONN.execute(
		C.CT.insert(), {
			"EntID": EntID,
			"OnColl": OnColl,
			"OffColl": OffColl,
		}
	)

def fetchT(EntID):
	return G.CONN.execute(
		C.CT	.select() \
			.where(C.CT.c.EntID == EntID)
	).fetchall()

def instancesT(EntID):
	return len(G.CONN.execute(
		C.CT.select().where(C.CT.c.EntID == EntID)
	).fetchall())

def deregisterT(EntID, OnColl, OffColl):
	G.CONN.execute(
		C.CT.delete().where(
			C.CT.c.EntID == EntID &
			C.CT.c.OnColl == OnColl &
			C.CT.c.OffColl == OffColl
		)
	)

def registerU(EntID):
	G.CONN.execute(
		C.CU.insert(), {
			"EntID": EntID,
		}
	)

def instancesU(EntID):
	return len(G.CONN.execute(
		C.CG.select().where(C.CG.c.EntID == EntID)
	).fetchall())

def deregisterU(EntID):
	G.CONN.execute(
		C.CG.delete().where(
			C.CG.c.EntID == EntID
		)
	)

def _getCollisions():
	collisions = set()
	
	global collQuery
	for TEntID, UEntID, TRectID, URectID, OnColl, OffColl in G.CONN.execute(collQuery).fetchall():
		if R.RR[TRectID].colliderect(R.RR[URectID]):
			# TODO: Check for 'collide by mask' as well
			collisions |= {(TEntID, UEntID, TRectID, URectID, OnColl, OffColl)} # We add in the collision handler indeces so that we don't have to perform another query at (1)
	
	return collisions

def update():
	global prevCollisions
	
	collisions = _getCollisions()
	
	newCollisions = collisions - prevCollisions
	oldCollisions = prevCollisions - collisions
	
	prevCollisions = collisions
	
	# (1)
	for TEntID, UEntID, TRectID, URectID, OnColl, OffColl in newCollisions:
		R.CR[OnColl](TEntID, UEntID, TRectID, URectID)
	
	# (1)
	for TEntID, UEntID, TRectID, URectID, OnColl, OffColl in oldCollisions:
		R.CR[OffColl](TEntID, UEntID, TRectID, URectID)
	
	for handler in R.CCR.values():
		handler()
