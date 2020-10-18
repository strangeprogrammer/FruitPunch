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

from .. import DebugTools

from ..Common.Misc import LevelLoadException
from ..Common import ExtraSerDes as ESD
from ..Common import Time

from . import (
	Events,
	G,
	Component as C,
	Resource as R,
	LevelLoader,
	Level,
	Radio,
)

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

def update():
	Radio.doController()
	
	for proxyID in Radio.proxies:
		Radio.queues[proxyID] = ["dodraw"]
	
	Radio.flush()
	
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
	
	Radio.doProxies()

def mainloop():
	fps = DebugTools.FPSPrinter(2000, "Server:      ")
	
	while G.ALIVE:
		try:
			update()
			fps.update()
		except LevelLoadException as e:
			Level.unload()
			Level.load(e.filename)

def _main(SERVCONTUP, SERVCONTDOWN):
	G.SERVCONTUP = SERVCONTUP
	G.SERVCONTDOWN = SERVCONTDOWN
	
	ESD.init()
	pg.init()
	
	Level.load("./LEVELS/tutorial.json")
	
	mainloop()
	
	Level.unload()
	
	pg.quit()
	ESD.quit()
	
	sys.exit(0)

### Profiling Specific

import cProfile as cpr
from ..Config import PROFILING

if PROFILING == True:
	def main(*args, **kwargs):
		cpr.runctx(
			"from src.Server.Server import _main;" + \
			"_main(*args, **kwargs);",
			globals = globals(),
			locals = {"args": args, "kwargs": kwargs},
			filename = "./Server.stats"
		)
else:
	main = _main
