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
import sqlalchemy as sqa
import sys

from . import (
	Events,
	G,
	Component as C,
	Resource as R,
	LevelLoader,
	Time,
	Level,
	Radio,
)

from .Misc import LevelLoadException

from .Systems import (
	Camera,
	Draw,
	Position,
	Rotation,
	Velocity,
	RotVel,
	Accel,
	Flip,
	FlipDoll,
	RotDoll,
	Strut,
	Collision,
)

import itertools
counter = itertools.count()

def update():
	Radio.update()
	
	Accel.update()
	Velocity.update()
	RotVel.update()
	
	FlipDoll.update()
	RotDoll.update()
	
	Draw.resetDrawComp()
	Draw.updateDrawComp(Flip.render())
	Draw.updateDrawComp(Rotation.render())
	Draw.updateRects()
	
	Position.update()
	
	Collision.update()
	
	Strut.update()
	Position.update() # I hate double-updating the positions, but this is the best way that I know of right now to make 'bumping' work smoothly with struts
	
#	Camera.update()
	
#	Draw.update()
	
	Rotation.collect()
	
	Time.update()
	
#	global counter
#	if next(counter) % 60 == 0:
#		print(Time._clock.get_fps())

def main(SERVTOCONT):
	G.SERVTOCONT = SERVTOCONT
	
	pg.init()
	
	Level.load("./LEVELS/tutorial.json")
	
	while G.ALIVE:
		try:
			update()
		except LevelLoadException as e:
			Level.unload()
			Level.load(e.filename)
	
	Level.unload()
	pg.quit()
	sys.exit(0)
