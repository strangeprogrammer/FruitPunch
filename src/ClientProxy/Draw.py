#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

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

from . import G
from ..Common.Misc import Rect

from . import Resource as R

from . import Camera as Cam

bgd = None

def quit():
	global bgd
	bgd = None

def _blackPad(bgd):
	badlands = Rect(bgd.get_rect()).cleanCrack(Cam.Cam)
	badlands = list(map(lambda r: r - Cam.Cam, badlands))
	outsurfaces = list(map(lambda r: G.SCREEN.subsurface(r), badlands))
	
	for s in outsurfaces:
		s.fill([0, 0, 0])

def update():
	global bgd
	
	# Draw the background first
	G.SCREEN.blit(bgd, (0, 0), Cam.Cam)
	_blackPad(bgd)
	
	# Draw all entities
	for [RectID, ImageID, Major, SubMajor, Minor] \
	in sorted(R.DR, key =
		lambda x: ".".join(map(str, x[2:]))
	):
		rect = R.RR[RectID]
		if rect.colliderect(Cam.Cam):
			G.SCREEN.blit(
				R.IR[ImageID],
				rect - Cam.Cam,
				Rect(0, 0, rect.width, rect.height)
			)
	
	pg.display.flip()
