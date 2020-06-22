#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import math

def radToDeg(theta):
	return theta * 360 / math.tau

def degToRad(theta):
	return theta * math.tau / 360
