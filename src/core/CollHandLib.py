#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from . import Resource as R

from .Systems import Position, Velocity

ejectUpID = ejectDownID = ejectLeftID = ejectRightID = ejectID = None

def init():
	global ejectUpID, ejectDownID, ejectLeftID, ejectRightID, ejectID
	ejectUpID	= R.CR.append(ejectUp)
	ejectDownID	= R.CR.append(ejectDown)
	ejectLeftID	= R.CR.append(ejectLeft)
	ejectRightID	= R.CR.append(ejectRight)
	ejectID		= R.CR.append(eject)

def _makeLines(rect1, collrect):
	"""Make diagonal lines of 'rect1' and the expected 'y' values of 'collrect' given those lines."""
	BRTL = {}
	TRBL = {}
	
	BRTL["m"] = (rect1.bottom - rect1.top) / (rect1.right - rect1.left)
	TRBL["m"] = -BRTL["m"] # This can be demonstrated geometrically using a rectangle in the coordinate plane
	
	BRTL["b"] = rect1.bottom - BRTL["m"] * rect1.right
	TRBL["b"] = rect1.top - TRBL["m"] * rect1.right
	
	BRTL["y"] = BRTL["m"] * collrect.centerx + BRTL["b"]
	TRBL["y"] = TRBL["m"] * collrect.centerx + TRBL["b"]
	
	return [BRTL, TRBL]

def eject(EntID, Ent2ID, RectID, Rect2ID):
	args = [EntID, Ent2ID, RectID, Rect2ID]
	
	ejectUp(*args)
	ejectDown(*args)
	ejectLeft(*args)
	ejectRight(*args)

def ejectUp(EntID, Ent2ID, RectID, Rect2ID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[RectID]
	rect2 = R.RR[Rect2ID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery <= BRTL["y"] and collrect.centery < TRBL["y"]:
		# Top Quadrant
		rect2.bottom = rect1.top
		Velocity.store(Ent2ID, Velocity.fetch(Ent2ID)[0], 0)
	
	Position.store(Ent2ID, *rect2.center)

def ejectDown(EntID, Ent2ID, RectID, Rect2ID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[RectID]
	rect2 = R.RR[Rect2ID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery >= BRTL["y"] and collrect.centery > TRBL["y"]:
		# Bottom Quadrant
		rect2.top = rect1.bottom
		Velocity.store(Ent2ID, Velocity.fetch(Ent2ID)[0], 0)
	
	Position.store(Ent2ID, *rect2.center)

def ejectLeft(EntID, Ent2ID, RectID, Rect2ID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[RectID]
	rect2 = R.RR[Rect2ID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery > BRTL["y"] and collrect.centery <= TRBL["y"]:
		# Left Quadrant
		rect2.right = rect1.left
		Velocity.store(Ent2ID, 0, Velocity.fetch(Ent2ID)[1])
	
	Position.store(Ent2ID, *rect2.center)

def ejectRight(EntID, Ent2ID, RectID, Rect2ID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[RectID]
	rect2 = R.RR[Rect2ID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery < BRTL["y"] and collrect.centery >= TRBL["y"]:
		# Right Quadrant
		rect2.left = rect1.right
		Velocity.store(Ent2ID, 0, Velocity.fetch(Ent2ID)[1])
	
	Position.store(Ent2ID, *rect2.center)
