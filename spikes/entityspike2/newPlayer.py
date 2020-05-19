#!/bin/python3

from pygame.image import load as LD
import math

from physBodies.bodies import rotationBody
from Entity import Entity
from ConflictMonitor import SymmetricConflictMonitor as SCM

### Animations

def twistBox(box, moment):
	box.theta = math.sin(moment / 1000) * math.pi / 4

def boxDown(box, moment, duration):
	box.rect.centery = 100 + (200 - 100) * (moment / duration)

def boxUp(box, moment, duration):
	box.rect.centery = 200 - (200 - 100) * (moment / duration)

### Brain

def startBox(ent, boxName, worldTime, **worldState):
	"""Spams the start button for the animation"""
	ent.startAnim("twist" + boxName, worldTime, math.tau * 1000)

def pushBox(ent, actions, boxName, state, worldTime, **worldState):
	"""Pushes the start button for the animation if required"""
	animName = boxName + "Down"
	if animName in actions and not state[boxName]:
		ent.startAnim(animName, worldTime, 2000)

def pullBox(ent, actions, boxName, state, worldTime, **worldState):
	"""Pushes the start button for the animation if required"""
	animName = boxName + "Up"
	if animName in actions and state[boxName]:
		ent.startAnim(animName, worldTime, 2000)

def cullPush(ent, boxName, state):
	animName = boxName + "Down"
	if animName in ent.culledAnims:
		state[boxName] = not state[boxName]

def cullPull(ent, boxName, state):
	animName = boxName + "Up"
	if animName in ent.culledAnims:
		state[boxName] = not state[boxName]

def brain(): # Note: We construct a stateful brain using a closure (maybe could be extended using finite state machines?)
	state = {
		"R": False,
		"B": False,
		"G": False,
		"Y": False,
	}
	
	def retval(ent, actions, **worldState):
		startBox(ent, "R", **worldState)
		startBox(ent, "B", **worldState)
		startBox(ent, "G", **worldState)
		startBox(ent, "Y", **worldState)
		
		# TODO (next commit): Lock down animations by making them conflict with a permanent animation called 'reality'?
		cullPush(ent, "R", state)
		cullPush(ent, "B", state)
		cullPush(ent, "G", state)
		cullPush(ent, "Y", state)
		
		cullPull(ent, "R", state)
		cullPull(ent, "B", state)
		cullPull(ent, "G", state)
		cullPull(ent, "Y", state)
		
		pushBox(ent, actions, "R", state, **worldState)
		pushBox(ent, actions, "B", state, **worldState)
		pushBox(ent, actions, "G", state, **worldState)
		pushBox(ent, actions, "Y", state, **worldState)
		
		pullBox(ent, actions, "R", state, **worldState)
		pullBox(ent, actions, "B", state, **worldState)
		pullBox(ent, actions, "G", state, **worldState)
		pullBox(ent, actions, "Y", state, **worldState)
	
	return retval

### Player Creation

def newPlayer():
	corpus = {
		"R": rotationBody(image = LD("../RESOURCES/RedSquare.png"), center = (100, 100)),
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
	
	scm = SCM(conflicts = {
		"RDown":	{"RDown", "RUp"},
		"BDown":	{"BDown", "BUp"},
		"GDown":	{"GDown", "GUp"},
		"YDown":	{"YDown", "YUp"},
		"RUp":		{"RDown", "RUp"},
		"BUp":		{"BDown", "BUp"},
		"GUp":		{"GDown", "GUp"},
		"YUp":		{"YDown", "YUp"},
		"twistR":	{"twistR"},
		"twistB":	{"twistB"},
		"twistG":	{"twistG"},
		"twistY":	{"twistY"},
	})
	
	return Entity(
		corpus = corpus,
		animations = animations,
		scm = scm,
		brain = brain(),
	)
