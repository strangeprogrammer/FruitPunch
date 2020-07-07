#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from . import Resource as R

from .Systems import Position, Velocity

onEjectUpID = onEjectDownID = onEjectLeftID = onEjectRightID = onEjectID = None
offEjectUpID = offEjectDownID = offEjectLeftID = offEjectRightID = offEjectID = None

def init():
	global onEjectUpID, onEjectDownID, onEjectLeftID, onEjectRightID, onEjectID
	onEjectUpID	= R.CR.append(onEjectUp)
	onEjectDownID	= R.CR.append(onEjectDown)
	onEjectLeftID	= R.CR.append(onEjectLeft)
	onEjectRightID	= R.CR.append(onEjectRight)
	onEjectID	= R.CR.append(onEject)
	
	global offEjectUpID, offEjectDownID, offEjectLeftID, offEjectRightID, offEjectID
	offEjectUpID	= R.CR.append(offEjectUp)
	offEjectDownID	= R.CR.append(offEjectDown)
	offEjectLeftID	= R.CR.append(offEjectLeft)
	offEjectRightID	= R.CR.append(offEjectRight)
	offEjectID	= R.CR.append(offEject)

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

def onEject(TEntID, UEntID, TRectID, URectID):
	args = [TEntID, UEntID, TRectID, URectID]
	
	onEjectUp(*args)
	onEjectDown(*args)
	onEjectLeft(*args)
	onEjectRight(*args)

def offEject(TEntID, UEntID, TRectID, URectID):
	args = [TEntID, UEntID, TRectID, URectID]
	
	offEjectUp(*args)
	offEjectDown(*args)
	offEjectLeft(*args)
	offEjectRight(*args)

def ejectUp(UEntID, rect1, rect2):
	rect2.bottom = rect1.top
	Velocity.store(UEntID, Velocity.fetch(UEntID)[0], 0)
	Position.store(UEntID, *rect2.center)

def onEjectUp(TEntID, UEntID, TRectID, URectID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[TRectID]
	rect2 = R.RR[URectID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery <= BRTL["y"] and collrect.centery < TRBL["y"]:
		R.CCR[(TEntID, UEntID, "ejectUp")] = lambda: ejectUp(UEntID, rect1, rect2)

def offEjectUp(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "ejectUp") in R.CCR.members.keys():
		del R.CCR[(TEntID, UEntID, "ejectUp")]

def ejectDown(UEntID, rect1, rect2):
	rect2.top = rect1.bottom
	Velocity.store(UEntID, Velocity.fetch(UEntID)[0], 0)
	Position.store(UEntID, *rect2.center)

def onEjectDown(TEntID, UEntID, TRectID, URectID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[TRectID]
	rect2 = R.RR[URectID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery >= BRTL["y"] and collrect.centery > TRBL["y"]:
		R.CCR[(TEntID, UEntID, "ejectDown")] = lambda: ejectDown(UEntID, rect1, rect2)

def offEjectDown(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "ejectDown") in R.CCR.members.keys():
		del R.CCR[(TEntID, UEntID, "ejectDown")]

def ejectLeft(UEntID, rect1, rect2):
	rect2.right = rect1.left
	Velocity.store(UEntID, 0, Velocity.fetch(UEntID)[1])
	Position.store(UEntID, *rect2.center)

def onEjectLeft(TEntID, UEntID, TRectID, URectID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[TRectID]
	rect2 = R.RR[URectID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery > BRTL["y"] and collrect.centery <= TRBL["y"]:
		R.CCR[(TEntID, UEntID, "ejectLeft")] = lambda: ejectLeft(UEntID, rect1, rect2)

def offEjectLeft(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "ejectLeft") in R.CCR.members.keys():
		del R.CCR[(TEntID, UEntID, "ejectLeft")]

def ejectRight(UEntID, rect1, rect2):
	rect2.left = rect1.right
	Velocity.store(UEntID, 0, Velocity.fetch(UEntID)[1])
	Position.store(UEntID, *rect2.center)

def onEjectRight(TEntID, UEntID, TRectID, URectID):
	"""Eject the 2nd entity based upon diagonally divided quadrants of the 1st entity."""
	
	rect1 = R.RR[TRectID]
	rect2 = R.RR[URectID]
	collrect = rect2.clip(rect1.clip(rect2))
	
	[BRTL, TRBL] = _makeLines(rect1, collrect)
	
	if collrect.centery < BRTL["y"] and collrect.centery >= TRBL["y"]:
		R.CCR[(TEntID, UEntID, "ejectRight")] = lambda: ejectRight(UEntID, rect1, rect2)

def offEjectRight(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "ejectRight") in R.CCR.members.keys():
		del R.CCR[(TEntID, UEntID, "ejectRight")]
