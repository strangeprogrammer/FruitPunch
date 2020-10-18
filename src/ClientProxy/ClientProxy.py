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
import sys

from .. import DebugTools

from ..Common import ExtraSerDes as ESD
from ..Common import Time

from . import (
	G,
	Camera,
	Draw,
#	Events,
	Radio,
	Resource as R,
)

def update():
	Radio.doServer()
	Radio.flush()
	
#	Events.update()
	Camera.update()
	
	Draw.update(R.DR.copy(), R.RR.copy(), R.IR.copy()) # Duplicate these resources since they might be overwritten by the Radio
	
	Time.update()

def mainloop():
	fps = DebugTools.FPSPrinter(2000, "ClientProxy: ")
	
	while G.ALIVE:
		update()
		fps.update()

def _main(CLISERVUP, CLISERVDOWN):
	G.CLISERVUP = CLISERVUP
	G.CLISERVDOWN = CLISERVDOWN
	
	pg.init()
	ESD.init()
	
	Camera.init()
	
	Radio.cmdqueue.append("getimages")
	Radio.cmdqueue.append("getbgd")
	Radio.cmdqueue.append("getplayerid")
	
	Time.init()
	
	while not Radio.drawReady:
		Radio.doServer()
	
	mainloop()
	
	Camera.quit()
	Draw.quit()
	
	ESD.quit()
	pg.quit()
	
	sys.exit(0)

### Profiling Specific

import cProfile as cpr
from ..Config import PROFILING

if PROFILING == True:
	def main(*args, **kwargs):
		cpr.runctx(
			"from src.ClientProxy.ClientProxy import _main;" + \
			"_main(*args, **kwargs);",
			globals = globals(),
			locals = {"args": args, "kwargs": kwargs},
			filename = "./ClientProxy.stats"
		)
else:
	main = _main
