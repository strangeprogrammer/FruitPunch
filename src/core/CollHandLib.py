#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from . import Resource as R

from .Systems import Position, Velocity

onEjectUpID = onEjectDownID = onEjectLeftID = onEjectRightID = None
offEjectUpID = offEjectDownID = offEjectLeftID = offEjectRightID = None

def init():
	global onEjectUpID, onEjectDownID, onEjectLeftID, onEjectRightID
	onEjectUpID	= R.CR.append(onEjectUp)
	onEjectDownID	= R.CR.append(onEjectDown)
	onEjectLeftID	= R.CR.append(onEjectLeft)
	onEjectRightID	= R.CR.append(onEjectRight)
	
	global offEjectUpID, offEjectDownID, offEjectLeftID, offEjectRightID
	offEjectUpID	= R.CR.append(offEjectUp)
	offEjectDownID	= R.CR.append(offEjectDown)
	offEjectLeftID	= R.CR.append(offEjectLeft)
	offEjectRightID	= R.CR.append(offEjectRight)

def _makeLines(trect, collrect):
	"""Make diagonal lines of 'trect' and the expected 'y' values of 'collrect' given those lines."""
	BRTL = {}
	TRBL = {}
	
	BRTL["m"] = (trect.bottom - trect.top) / (trect.right - trect.left)
	TRBL["m"] = -BRTL["m"] # This can be demonstrated geometrically using a rectangle in the coordinate plane
	
	BRTL["b"] = trect.bottom - BRTL["m"] * trect.right
	TRBL["b"] = trect.top - TRBL["m"] * trect.right
	
	BRTL["y"] = BRTL["m"] * collrect.centerx + BRTL["b"]
	TRBL["y"] = TRBL["m"] * collrect.centerx + TRBL["b"]
	
	return [BRTL, TRBL]

def ejectSetup(f):
	def wrapper(TEntID, UEntID, TRectID, URectID):
		"""Eject the untriggered entity based upon diagonally divided quadrants of the triggered entity."""
		
		trect = R.RR[TRectID]
		urect = R.RR[URectID]
		collrect = urect.clip(trect)
		
		if collrect.isValid(): # The untriggered entity could've been moved by another eject handler before this one, leaving the clipping area empty
			[BRTL, TRBL] = _makeLines(trect, collrect)
			
			f(UEntID, trect, urect, collrect, BRTL, TRBL)
			
			Position.store(UEntID, urect.centerx, urect.centery)
	
	return wrapper



@ejectSetup
def ejectUp(UEntID, trect, urect, collrect, BRTL, TRBL):
	if collrect.centery <= BRTL["y"] and collrect.centery < TRBL["y"]:
		urect.bottom = trect.top
		Velocity.store(UEntID, Velocity.fetch(UEntID)[0], 0)

@ejectSetup
def ejectDown(UEntID, trect, urect, collrect, BRTL, TRBL):
	if collrect.centery >= BRTL["y"] and collrect.centery > TRBL["y"]:
		urect.top = trect.bottom
		Velocity.store(UEntID, Velocity.fetch(UEntID)[0], 0)

@ejectSetup
def ejectLeft(UEntID, trect, urect, collrect, BRTL, TRBL):
	if collrect.centery > BRTL["y"] and collrect.centery <= TRBL["y"]:
		urect.right = trect.left
		Velocity.store(UEntID, 0, Velocity.fetch(UEntID)[1])

@ejectSetup
def ejectRight(UEntID, trect, urect, collrect, BRTL, TRBL):
	if collrect.centery < BRTL["y"] and collrect.centery >= TRBL["y"]:
		urect.left = trect.right
		Velocity.store(UEntID, 0, Velocity.fetch(UEntID)[1])



def onEjectUp(TEntID, UEntID, TRectID, URectID):
	R.CCR[(TEntID, UEntID, "ejectUp")] = lambda: ejectUp(TEntID, UEntID, TRectID, URectID)

def onEjectDown(TEntID, UEntID, TRectID, URectID):
	R.CCR[(TEntID, UEntID, "ejectDown")] = lambda: ejectDown(TEntID, UEntID, TRectID, URectID)

def onEjectLeft(TEntID, UEntID, TRectID, URectID):
	R.CCR[(TEntID, UEntID, "ejectLeft")] = lambda: ejectLeft(TEntID, UEntID, TRectID, URectID)

def onEjectRight(TEntID, UEntID, TRectID, URectID):
	R.CCR[(TEntID, UEntID, "ejectRight")] = lambda: ejectRight(TEntID, UEntID, TRectID, URectID)



def offEjectUp(TEntID, UEntID, TRectID, URectID):
	del R.CCR[(TEntID, UEntID, "ejectUp")]

def offEjectDown(TEntID, UEntID, TRectID, URectID):
	del R.CCR[(TEntID, UEntID, "ejectDown")]

def offEjectLeft(TEntID, UEntID, TRectID, URectID):
	del R.CCR[(TEntID, UEntID, "ejectLeft")]

def offEjectRight(TEntID, UEntID, TRectID, URectID):
	del R.CCR[(TEntID, UEntID, "ejectRight")]
