#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import ResPack

from . import Component as C

ER = IR = RR = CR = CCR = None

def init():
	global ER, IR, RR, CR, CCR
	
	ER	= ResPack(table = C.E, field = "EntID")
	IR	= ResPack(table = C.I, field = "ImageID")
	RR	= ResPack(table = C.R, field = "RectID")
	CR	= ResPack()
	CCR	= ResPack()

def quit():
	global ER, IR, RR, CR, CCR
	ER = IR = RR = CR = CCR = None
