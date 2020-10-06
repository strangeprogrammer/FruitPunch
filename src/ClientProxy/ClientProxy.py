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

from . import (
	G,
	Camera,
	Draw,
#	Events,
)

from . import G
from . import Radio

from ..Common import ExtraSerDes as ESD

from . import Resource as R

#from itertools import count
#cycles = count()

def update():
	Radio.cmdqueue.append("getrects")
	Radio.cmdqueue.append("getdrawn")
	
	Radio.update()
	
#	Events.update()
	Camera.update()
	Draw.update()
	
#	global cycles
#	cyclex = next(cycles)
#	if cyclex % 100 == 0:
#		import pprint
#		pprint.pprint(R.RR)

def main(CLITOSERV):
	G.CLITOSERV = CLITOSERV
	
	pg.init()
	ESD.init()
	
	Camera.init()
	
	Radio.cmdqueue.append("getimages")
	Radio.cmdqueue.append("getbgd")
	Radio.cmdqueue.append("getplayerid")
	
	while G.ALIVE:
		update()
	
	Camera.quit()
	Draw.quit()
	
	ESD.quit()
	pg.quit()
	
	sys.exit(0)
