#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import create

IR = RR = CR = None

def init():
	global IR, RR, YCR, NCR
	
	IR = create("ImageRes")
	RR = create("RectRes")
	YCR = create("OnCollRes")
	NCR = create("OffCollRes")
