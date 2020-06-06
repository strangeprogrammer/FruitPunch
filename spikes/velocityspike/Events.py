#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import pygame as pg

handlers = {}

def register(eventType, callback):
	global handlers
	handlers[eventType] = callback

def deregister(eventType):
	global handlers
	del handlers[eventType]

def update():
	global handlers
	for e in pg.event.get():
		handlers.get(e.type, lambda e: None)(e) # Switch on the event type and run its handler
