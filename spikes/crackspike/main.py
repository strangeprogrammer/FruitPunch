#!/bin/python3

import pygame as pg

from Crack import crack, getTangible

screen = pg.display.set_mode()
screen.fill( (255, 255, 255) )

from itertools import count
counter = count()

colors = [
	pg.Color(255, 0, 0),
	pg.Color(0, 255, 0),
	pg.Color(0, 0, 255),
	pg.Color(255, 255, 0),
	pg.Color(0, 255, 255),
	pg.Color(255, 0, 255),
	pg.Color(255, 128, 0),
	pg.Color(0, 255, 128),
	pg.Color(128, 0, 255),
	pg.Color(255, 0, 128),
	pg.Color(128, 255, 0),
	pg.Color(0, 128, 255),
]

x = pg.Rect(300, 300, 100, 100)
y = pg.Rect(200, 200, 300, 300)

pg.draw.rect(screen, (0, 0, 0), x)
for rect in getTangible(crack(x, y)):
	pg.draw.rect(screen, colors[next(counter)], rect)

pg.display.flip()

input()
