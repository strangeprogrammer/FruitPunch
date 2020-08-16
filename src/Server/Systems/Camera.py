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

from .. import Component as C
from .. import Resource as R

from .. import G
from ..Misc import Rect

from . import Position
from . import Velocity
from . import Rectangle

EntID = RectID = BindID = None

def init():
	global EntID, RectID
	
	G.SCREEN = pg.display.set_mode()
	rect = Rect(G.SCREEN.get_rect())
	(rect.x, rect.y) = (0, 0)
	
	RectID = R.RR.append(rect)
	R.RR.flush()
	
	EntID = R.ER.append(None)
	R.ER.flush()
	
	Rectangle.register(EntID)
	Rectangle.store(EntID, RectID)
	
	Position.register(EntID)
	Velocity.register(EntID)

def quit():
	unbind()
	
	global EntID, RectID
	
	Velocity.deregister(EntID)
	Position.deregister(EntID)
	
	Rectangle.deregister(EntID)
	
	del R.ER[EntID]
	R.ER.flush()
	
	del R.RR[RectID]
	R.RR.flush()
	
	G.SCREEN = None
	
	EntID = RectID = BindID = None

def fetch():
	global RectID
	rect = R.RR[RectID]
	return (rect.left, rect.top)

def store(left, top):
	global RectID
	rect = R.RR[RectID]
	rect.left = left
	rect.top = top

def bind(EntID):
	global BindID
	BindID = EntID

def unbind():
	global BindID
	BindID = None

def update():
	global RectID, BindID
	if BindID is not None:
		oldcenter = R.RR[RectID].center
		newcenter = R.RR[Rectangle.fetch(BindID)].center
		if oldcenter != newcenter:
			R.RR[RectID].center = newcenter
			R.RR.invalidate(RectID)
	
	R.RR.flush()
