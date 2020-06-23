#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from .ResPack import create

IR = RR = YCR = WCR = NCR = None

def init():
	global IR, RR, YCR, WCR, NCR
	
	IR = create("ImageRes")
	RR = create("RectRes")
	YCR = create("OnCollRes")
	WCR = create("WhileCollRes")
	NCR = create("OffCollRes")
