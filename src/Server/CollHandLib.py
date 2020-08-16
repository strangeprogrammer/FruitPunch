#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

# Copyright (C) 2020 Stephen Fedele <32551324+strangeprogrammer@users.noreply.github.com>
# 
# This file is part of Fruit Punch.
# 
# Fruit Punch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Fruit Punch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Fruit Punch.  If not, see <https://www.gnu.org/licenses/>.
# 
# Additional terms apply to this file.  Read the file 'LICENSE.txt' for
# more information.



from . import Resource as R

from . import Time
from .Misc import LevelLoadException

from .Systems import Position, Velocity

onEjectUpID = onEjectDownID = onEjectLeftID = onEjectRightID = None
offEjectUpID = offEjectDownID = offEjectLeftID = offEjectRightID = None

onOneWayUpID = onOneWayDownID = onOneWayLeftID = onOneWayRightID = None
offOneWayUpID = offOneWayDownID = offOneWayLeftID = offOneWayRightID = None

onDoorID = None

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
	
	global onOneWayUpID, onOneWayDownID, onOneWayLeftID, onOneWayRightID
	onOneWayUpID	= R.CR.append(onOneWayUp)
	onOneWayDownID	= R.CR.append(onOneWayDown)
	onOneWayLeftID	= R.CR.append(onOneWayLeft)
	onOneWayRightID	= R.CR.append(onOneWayRight)
	
	global offOneWayUpID, offOneWayDownID, offOneWayLeftID, offOneWayRightID
	offOneWayUpID		= R.CR.append(offOneWayUp)
	offOneWayDownID		= R.CR.append(offOneWayDown)
	offOneWayLeftID		= R.CR.append(offOneWayLeft)
	offOneWayRightID	= R.CR.append(offOneWayRight)
	
	global onDoorID
	onDoorID	 = R.CR.append(onDoor)

def quit():
	global onEjectUpID, onEjectDownID, onEjectLeftID, onEjectRightID
	global offEjectUpID, offEjectDownID, offEjectLeftID, offEjectRightID
	onEjectUpID = onEjectDownID = onEjectLeftID = onEjectRightID = None
	offEjectUpID = offEjectDownID = offEjectLeftID = offEjectRightID = None
	
	global onOneWayUpID, onOneWayDownID, onOneWayLeftID, onOneWayRightID
	global offOneWayUpID, offOneWayDownID, offOneWayLeftID, offOneWayRightID
	onOneWayUpID = onOneWayDownID = onOneWayLeftID = onOneWayRightID = None
	offOneWayUpID = offOneWayDownID = offOneWayLeftID = offOneWayRightID = None
	
	global onDoorID
	onDoorID = None

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



def onOneWayUp(TEntID, UEntID, TRectID, URectID):
	[VelX, VelY] = Velocity.fetch(UEntID)
	trect = R.RR[TRectID]
	urect = R.RR[URectID]
	
	if 0 < VelY and urect.bottom - Time.elapsed * VelY - 1 < trect.top: # The '1' is to account for rounding errors due to the velocity update step
		R.CCR[(TEntID, UEntID, "oneWayUp")] = lambda: ejectUp(TEntID, UEntID, TRectID, URectID)

def onOneWayDown(TEntID, UEntID, TRectID, URectID):
	[VelX, VelY] = Velocity.fetch(UEntID)
	trect = R.RR[TRectID]
	urect = R.RR[URectID]
	
	if VelY < 0 and trect.bottom < urect.top - Time.elapsed * VelY - 1: # The '1' is to account for rounding errors due to the velocity update step
		R.CCR[(TEntID, UEntID, "oneWayDown")] = lambda: ejectDown(TEntID, UEntID, TRectID, URectID)

def onOneWayLeft(TEntID, UEntID, TRectID, URectID):
	[VelX, VelY] = Velocity.fetch(UEntID)
	trect = R.RR[TRectID]
	urect = R.RR[URectID]
	
	if 0 < VelX and urect.right - Time.elapsed * VelX - 1 < trect.left: # The '1' is to account for rounding errors due to the velocity update step
		R.CCR[(TEntID, UEntID, "oneWayLeft")] = lambda: ejectLeft(TEntID, UEntID, TRectID, URectID)

def onOneWayRight(TEntID, UEntID, TRectID, URectID):
	[VelX, VelY] = Velocity.fetch(UEntID)
	trect = R.RR[TRectID]
	urect = R.RR[URectID]
	
	if VelX < 0 and trect.right < urect.left - Time.elapsed * VelX - 1 : # The '1' is to account for rounding errors due to the velocity update step
		R.CCR[(TEntID, UEntID, "oneWayDown")] = lambda: ejectRight(TEntID, UEntID, TRectID, URectID)



def offOneWayUp(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "oneWayUp") in R.CCR:
		del R.CCR[(TEntID, UEntID, "oneWayUp")]

def offOneWayDown(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "oneWayDown") in R.CCR:
		del R.CCR[(TEntID, UEntID, "oneWayDown")]

def offOneWayLeft(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "oneWayLeft") in R.CCR:
		del R.CCR[(TEntID, UEntID, "oneWayLeft")]

def offOneWayRight(TEntID, UEntID, TRectID, URectID):
	if (TEntID, UEntID, "oneWayRight") in R.CCR:
		del R.CCR[(TEntID, UEntID, "oneWayRight")]



def onDoor(TEntID, UEntID, TRectID, URectID):
	raise LevelLoadException(R.AAR[TEntID]["filename"])
