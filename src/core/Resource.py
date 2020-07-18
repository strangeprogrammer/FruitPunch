#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import ResPack

from . import Component as C

ER = IR = RR = CR = CCR = AAR = None

def init():
	global ER, IR, RR, CR, CCR, AAR
	
	ER	= ResPack(table = C.E, field = "EntID")		# Entity Resource
	IR	= ResPack(table = C.I, field = "ImageID")	# Image Resource
	RR	= ResPack(table = C.R, field = "RectID")	# Rectangle Resource
	CR	= ResPack()					# Collision Resource
	CCR	= ResPack()					# Continuous Collision Resource
	AAR	= ResPack()					# Auxilliary Attribute Resource

def quit():
	global ER, IR, RR, CR, CCR, AAR
	ER = IR = RR = CR = CCR = AAR = None
