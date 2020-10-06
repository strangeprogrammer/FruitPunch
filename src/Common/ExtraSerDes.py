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

from .Misc import Rect

from .ToBeGreen import (
	SD,
	Ser,
	Des,
)

def _pgs_ser(x):
	return Ser([
		pg.image.tostring(x, "RGBA"),
		x.get_size(),
	])

def _pgs_des(bobj):
	return pg.image.fromstring(*Des(bobj), "RGBA")

def _rect_ser(x):
	return Ser([
		x.left,
		x.top,
		x.width,
		x.height,
	])

def _rect_des(bobj):
	return Rect(*Des(bobj))

def init():
	SD.serers[pg.Surface] = [pg.Surface.__name__, _pgs_ser]
	SD.desers[pg.Surface.__name__] = _pgs_des
	SD.serers[Rect] = [Rect.__name__, _rect_ser]
	SD.desers[Rect.__name__] = _rect_des

def quit():
	del SD.serers[pg.Surface]
	del SD.desers[pg.Surface.__name__]
	del SD.serers[Rect]
	del SD.desers[Rect.__name__]
