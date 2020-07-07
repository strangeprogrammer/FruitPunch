#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import create

IR = RR = CR = CCR = None

def init():
	global IR, RR, CR, CCR
	
	IR = create("ImageRes")
	RR = create("RectRes")
	CR = create("CollRes")
	CCR = create("ContCollRes")
