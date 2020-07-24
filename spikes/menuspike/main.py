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

import menu

def main():
	pg.init()
	screen = pg.display.set_mode()
	
	menu.init()
	
	while True:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				pg.quit()
				return
			elif e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
				for i in menu.curMenu:
					if i.rect.collidepoint(e.pos):
						i.click()
		
		screen.fill( (255, 255, 255) )
		menu.curMenu.draw(screen)
		pg.display.flip()

main()
