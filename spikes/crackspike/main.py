#!/bin/python3

# Copyright (C) 2020 Stephen Fedele <32551324+strangeprogrammer@users.noreply.github.com>
# 
# This file is part of Fruit Punch.
# 
# Fruit Punch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Fruit Punch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Fruit Punch.  If not, see <https://www.gnu.org/licenses/>.
# 
# Additional terms apply to this file.  Read the file 'LICENSE.txt' for
# more information.



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
