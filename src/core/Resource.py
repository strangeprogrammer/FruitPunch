#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import create

IR = RR = None

def init():
	global IR, RR
	
	IR = create("ImageRes")
	RR = create("RectRes")
