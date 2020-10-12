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

### Update Routines

def doServer():
	while G.CLISERVDOWN.poll():
		servercmds = Des(G.CLISERVDOWN.recv_bytes())
		assert Ver(servercmds, str), "Error: object received from CLISERVDOWN was: " + str(servercmds)
		for event in servercmds.split():
			assert event in _serverevents, "Error: invalid server event: " + str(command)
			_serverevents[event]()

cmdqueue = []

def flush():
	global cmdqueue
	
	if cmdqueue:
		G.CLISERVUP.send_bytes(Ser(" ".join(cmdqueue)))
	
	for command in cmdqueue:
		_clientcmds[command]()
	
	cmdqueue = []

### Server Radio Event Routines

drawReady = False

def dodraw():
	drawinfo = Des(G.CLISERVDOWN.recv_bytes())
	rectinfo = Des(G.CLISERVDOWN.recv_bytes())
	
	assert Ver(drawinfo, V.LIST(
		V.PRODUCT(
			int,
			int,
			int,
			int,
			int,
		)
	)), "Error: response was: " + str(drawinfo)
	assert Ver(rectinfo, V.DICT(V.PRODUCT(int, Rect))), "Error: response was: " + str(rectinfo)
	
	R.DR = drawinfo
	R.RR = rectinfo
	
	global drawReady
	drawReady = True

_serverevents = {
	"dodraw":	dodraw,
}

### Client Radio Commands

def getimages():
	response = Des(G.CLISERVUP.recv_bytes())
	assert Ver(response, V.DICT(V.PRODUCT(int, pg.Surface))), "Error: response was: " + str(response)
	R.IR = response

def getbgd():
	response = Des(G.CLISERVUP.recv_bytes())
	assert Ver(response, pg.Surface), "Error: response was: " + str(response)
	Draw.bgd = response

def getplayerid():
	response = Des(G.CLISERVUP.recv_bytes())
	assert Ver(response, int), "Error: response was: " + str(response)
	Camera.bind(response)

_clientcmds = {
	"getimages":	getimages,
	"getbgd":	getbgd,
	"getplayerid":	getplayerid,
}
