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

from makeBodies import makeBodies

def main():
	pg.init()
	
	screen = pg.display.set_mode()
	screen.fill((255, 255, 255))
	bgd = screen.copy()
	pg.display.flip()
	bodies = makeBodies()
	
	goflag = True
	while goflag:
		bodies.update(pg.time.get_ticks() / 1000)
		pg.display.update(bodies.draw(screen))
		bodies.clear(screen, bgd)
		
		for e in pg.event.get():
			if e.type == pg.QUIT:
				goflag = False
				break
	
	pg.quit()

main()
