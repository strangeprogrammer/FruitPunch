#!/bin/python3

from pygame.image import load as LD
import math

from physBodies.bodies import rotationBody
from entity import entity

def listRemove(l, value):
	try:
		l.remove(value)
	except Exception:
		pass

### Animations

def twistBox(box, moment):
	box.theta = math.sin(moment / 1000) * math.pi / 4

def boxDown(box, moment, duration):
	box.rect.centery = 100 + (200 - 100) * (moment / duration)

def boxUp(box, moment, duration):
	box.rect.centery = 200 - (200 - 100) * (moment / duration)

### Actions

def startBox(ent, boxName, worldTime, **worldState):
	ent.startAnim("twist" + boxName, worldTime, math.tau * 1000)

def pushBox(ent, boxName, worldTime, **worldState):
	animName = boxName + "Down"
	moving = boxName + "Moving"
	if not (moving in ent.state or animName in ent.state):
		ent.startAnim(animName, worldTime, 2000)
		ent.state[animName] = True
		ent.state[moving] = True
		ent.state.pop(boxName + "Up", None)

def pullBox(ent, boxName, worldTime, **worldState):
	animName = boxName + "Up"
	moving = boxName + "Moving"
	if not (moving in ent.state or animName in ent.state):
		ent.startAnim(animName, worldTime, 2000)
		ent.state[animName] = True
		ent.state[moving] = True
		ent.state.pop(boxName + "Down", None)

### Brain

def twistRenew(culledAnims, retval, boxName):
	animName = "twist" + boxName
	if animName in culledAnims:
		retval.append(animName)

def boxRenew(ent, culledAnims, retval, boxName):
	anim1 = boxName + "Down"
	anim2 = boxName + "Up"
	moving = boxName + "Moving"
	
	if anim1 in culledAnims:
		ent.state.pop(moving, None)
	
	if anim2 in culledAnims:
		ent.state.pop(moving, None)

def brain(ent, actions, culledAnims, worldTime, **worldState):
	retval = actions
	
	twistRenew(culledAnims, retval, "R")
	twistRenew(culledAnims, retval, "B")
	twistRenew(culledAnims, retval, "G")
	twistRenew(culledAnims, retval, "Y")
	
	boxRenew(ent, culledAnims, retval, "R")
	boxRenew(ent, culledAnims, retval, "B")
	boxRenew(ent, culledAnims, retval, "G")
	boxRenew(ent, culledAnims, retval, "Y")
	
	return retval

def init(ent): # These technically aren't necessary for this case, but useful to observe nontheless
	ent.state["RUp"] = True
	ent.state["BUp"] = True
	ent.state["GUp"] = True
	ent.state["YUp"] = True

def newPlayer():
	corpus = {	"R": rotationBody(image = LD("../RESOURCES/RedSquare.png"), center = (100, 100)),
			"B": rotationBody(image = LD("../RESOURCES/BlueSquare.png"), center = (200, 100)),
			"G": rotationBody(image = LD("../RESOURCES/GreenSquare.png"), center = (300, 100)),
			"Y": rotationBody(image = LD("../RESOURCES/YellowSquare.png"), center = (400, 100)),
	}
	
	animations = {
			"RDown":	lambda corpus, moment, duration: boxDown(corpus["R"], moment, duration),
			"BDown":	lambda corpus, moment, duration: boxDown(corpus["B"], moment, duration),
			"GDown":	lambda corpus, moment, duration: boxDown(corpus["G"], moment, duration),
			"YDown":	lambda corpus, moment, duration: boxDown(corpus["Y"], moment, duration),
			"RUp":		lambda corpus, moment, duration: boxUp(corpus["R"], moment, duration),
			"BUp":		lambda corpus, moment, duration: boxUp(corpus["B"], moment, duration),
			"GUp":		lambda corpus, moment, duration: boxUp(corpus["G"], moment, duration),
			"YUp":		lambda corpus, moment, duration: boxUp(corpus["Y"], moment, duration),
			"twistR":	lambda corpus, moment, duration: twistBox(corpus["R"], moment),
			"twistB":	lambda corpus, moment, duration: twistBox(corpus["B"], moment),
			"twistG":	lambda corpus, moment, duration: twistBox(corpus["G"], moment),
			"twistY":	lambda corpus, moment, duration: twistBox(corpus["Y"], moment),
	}
	
	actions = {
			"RDown":	lambda ent, **worldState: pushBox(ent, "R", **worldState),
			"BDown":	lambda ent, **worldState: pushBox(ent, "B", **worldState),
			"GDown":	lambda ent, **worldState: pushBox(ent, "G", **worldState),
			"YDown":	lambda ent, **worldState: pushBox(ent, "Y", **worldState),
			"RUp":		lambda ent, **worldState: pullBox(ent, "R", **worldState),
			"BUp":		lambda ent, **worldState: pullBox(ent, "B", **worldState),
			"GUp":		lambda ent, **worldState: pullBox(ent, "G", **worldState),
			"YUp":		lambda ent, **worldState: pullBox(ent, "Y", **worldState),
			"twistR":	lambda ent, **worldState: startBox(ent, "R", **worldState),
			"twistB":	lambda ent, **worldState: startBox(ent, "B", **worldState),
			"twistG":	lambda ent, **worldState: startBox(ent, "G", **worldState),
			"twistY":	lambda ent, **worldState: startBox(ent, "Y", **worldState),
	}
	
	return entity(	corpus = corpus,
			animations = animations,
			actions = actions,
			brain = brain,
			init = init,
	)
