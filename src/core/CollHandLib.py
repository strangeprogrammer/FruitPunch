#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from . import Resource as R

from .Systems import Position, Velocity

ejectUpID = ejectDownID = ejectLeftID = ejectRightID = None

def init():
	global ejectUpID, ejectDownID, ejectLeftID, ejectRightID
	ejectUpID = R.CR.append(ejectUp)
	ejectDownID = R.CR.append(ejectDown)
	ejectLeftID = R.CR.append(ejectLeft)
	ejectRightID = R.CR.append(ejectRight)

def ejectUp(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.bottom = Rect1.top
	Position.store(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.fetch(Ent2ID)
	Velocity.store(Ent2ID, VelX, min(0, VelY))

def ejectDown(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.top = Rect1.bottom
	Position.store(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.fetch(Ent2ID)
	Velocity.store(Ent2ID, VelX, max(0, VelY))

def ejectLeft(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.right = Rect1.left
	Position.store(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.fetch(Ent2ID)
	Velocity.store(Ent2ID, min(0, VelX), VelY)

def ejectRight(EntID, Ent2ID, RectID, Rect2ID):
	Rect1 = R.RR[RectID]
	Rect2 = R.RR[Rect2ID]
	
	# if Rect1.colliderect(Rect2): # We assume this is true
	Rect2.left = Rect1.right
	Position.store(Ent2ID, Rect2.centerx, Rect2.centery)
	
	(VelX, VelY) = Velocity.fetch(Ent2ID)
	Velocity.store(Ent2ID, max(0, VelX), VelY)
