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



### Imports

import pygame as pg

from . import G
from . import Resource as R
from . import Draw
from . import Camera

from ..Common.ToBeGreen import (
	Ser,
	V,
	Ver,
	Des,
)
from ..Common.Misc import Rect

### Main loop

cmdqueue = []

def update():
	global cmdqueue
	
	if cmdqueue:
		G.CLITOSERV.send_bytes(Ser(' '.join(cmdqueue)))
	
	for cmdname in cmdqueue:
		assert cmdname in _allcmds, "Attempted to call an invalid radio command..."
		globals()[cmdname]()
	
	cmdqueue = []

### Radio Commands

_allcmds = [
	"getdrawn",
	"getimages",
	"getrects",
	"getbgd",
	"getplayerid",
]

def getdrawn():
	response = Des(G.CLITOSERV.recv_bytes())
	assert Ver(response, V.LIST(
		V.PRODUCT(
			int,
			int,
			int,
			int,
			int,
		)
	)), "Error: response was: " + str(response)
	R.DR = response

def getimages():
	response = Des(G.CLITOSERV.recv_bytes())
	assert Ver(response, V.DICT(V.PRODUCT(int, pg.Surface))), "Error: response was: " + str(response)
	R.IR = response

def getrects():
	response = Des(G.CLITOSERV.recv_bytes())
	assert Ver(response, V.DICT(V.PRODUCT(int, Rect))), "Error: response was: " + str(response)
	R.RR = response

def getbgd():
	response = Des(G.CLITOSERV.recv_bytes())
	assert Ver(response, pg.Surface), "Error: response was: " + str(response)
	Draw.bgd = response

def getplayerid():
	response = Des(G.CLITOSERV.recv_bytes())
	assert Ver(response, int), "Error: response was: " + str(response)
	Camera.bind(response)
