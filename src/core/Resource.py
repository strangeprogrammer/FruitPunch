#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import create

ER = IR = RR = CR = CCR = None

def init():
	global ER, IR, RR, CR, CCR
	
	ER = create("EntityRes")
	IR = create("ImageRes")
	RR = create("RectRes")
	CR = create("CollRes")
	CCR = create("ContCollRes")
