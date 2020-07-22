#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import ResPack
from .Misc import incrementable

from . import Component as C

ER = IR = RR = CR = CCR = AAR = None

def init():
	global ER, IR, RR, CR, CCR, AAR
	
	ER = incrementable(ResPack( # Entity Resource
		table = C.E,
		keyCol = C.E.c.EntID,
		packager = lambda k, v: { # This is only an example for now
			"EntID": k
		}
	))
	
	IR = incrementable(ResPack( # Image Resource
		table = C.I,
		keyCol = C.I.c.ImageID,
		packager = lambda k, v: { # This is only an example for now
			"ImageID": k
		}
	))
	
	RR = incrementable(ResPack( # Rectangle Resource
		table = C.R,
		keyCol = C.R.c.RectID,
		packager = lambda k, v: { # This is only an example for now
			"RectID": k
		}
	))
	
	class Dict(dict): # https://stackoverflow.com/a/2827664
		pass
	
	CR	= incrementable(Dict()) # Collision Resource
	CCR	= incrementable(Dict()) # Continuous Collision Resource
	AAR	= incrementable(Dict()) # Auxilliary Attribute Resource

def quit():
	global ER, IR, RR, CR, CCR, AAR
	ER = IR = RR = CR = CCR = AAR = None
