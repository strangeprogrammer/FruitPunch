#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

_clock = None
elapsed = now = 0

def init():
	global _clock
	_clock = pg.time.Clock()

def update():
	global _clock, elapsed, now
	elapsed = _clock.tick(60)
	now += elapsed
