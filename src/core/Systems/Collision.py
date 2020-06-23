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
	R.YCR[0] = lambda E1, E2, R1, R2: None	# Default on and off collision handlers do nothing
	R.NCR[0] = lambda E1, E2, R1, R2: None	#
	R.WCR[0] = lambda E1, E2, R1, R2: None	#
	next(R.YCR.counter)			# Adjust resource indeces so we don't accidentally overwrite default handlers
	next(R.NCR.counter)			#
	next(R.WCR.counter)			#
	
	global collQuery
	
	CC2 = C.CC.alias()
	RECC2 = C.RECC.alias()
	t1 = C.CC.join(C.RECC, C.CC.c.EntID == C.RECC.c.EntID)
	t2 = CC2.join(RECC2, CC2.c.EntID == RECC2.c.EntID)
	
	collQuery = sqa.select([
		C.CC.c.EntID,
		CC2.c.EntID,
		C.RECC.c.RectID,
		RECC2.c.RectID,
		C.CC.c.OnColl,
		C.CC.c.WhileColl,
		C.CC.c.OffColl,
	]).select_from(
		t1.join(t2, sqa.literal(True))
	).where(
		C.CC.c.EntID != CC2.c.EntID # Objects can't collide with themselves (or at least, it makes programming simpler)
	).compile()

def register(EntID):
	G.CONN.execute(
		C.CC.insert(), {
			"EntID": EntID,
			"OnColl": 0,
			"WhileColl": 0,
			"OffColl": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.CC.select().where(C.CC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.CC.delete().where(C.CC.c.EntID == EntID)
	)

def get(EntID):
	return G.CONN.execute(
		C.CC	.select() \
			.where(C.CC.c.EntID == EntID)
	).fetchone()

def setState(EntID, OnColl, WhileColl, OffColl):
	G.CONN.execute(
		C.CC.update().where(C.CC.c.EntID == EntID), {
			"OnColl": OnColl,
			"WhileColl": WhileColl,
			"OffColl": OffColl,
		}
	)

def _getCollisions():
	collisions = set()
	
	global collQuery
	for EntID, Ent2ID, RectID, Rect2ID, OnColl, WhileColl, OffColl in G.CONN.execute(collQuery).fetchall():
		if R.RR[RectID].colliderect(R.RR[Rect2ID]):
			# TODO: Check for 'collide by mask' as well
			collisions |= {(EntID, Ent2ID, RectID, Rect2ID, OnColl, WhileColl, OffColl)} # We add in the collision handler indeces so that we don't have to perform another query at (1)
	
	return collisions

def update():
	global prevCollisions
	
	collisions = _getCollisions()
	
	newCollisions = collisions - prevCollisions
	curCollisions = collisions & prevCollisions
	oldCollisions = prevCollisions - collisions
	
	prevCollisions = collisions
	
	# (1)
	for EntID, Ent2ID, RectID, Rect2ID, OnColl, WhileColl, OffColl in newCollisions:
		R.YCR[OnColl](EntID, Ent2ID, RectID, Rect2ID)
	
	# (1)
	for EntID, Ent2ID, RectID, Rect2ID, OnColl, WhileColl, OffColl in curCollisions:
		R.WCR[WhileColl](EntID, Ent2ID, RectID, Rect2ID)
	
	# (1)
	for EntID, Ent2ID, RectID, Rect2ID, OnColl, WhileColl, OffColl in oldCollisions:
		R.NCR[OffColl](EntID, Ent2ID, RectID, Rect2ID)
