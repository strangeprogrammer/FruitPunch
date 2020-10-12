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
from itertools import count

from ..Common.ToBeGreen import (
	Ser,
	Ver,
	Des,
)

from . import G
from . import Resource as R
from . import Player
from .Systems import (
	Draw,
)

### Update Routines

proxies = {}
proxyGen = count()

def doController():
	while G.SERVCONTDOWN.poll():
		command = Des(G.SERVCONTDOWN.recv_bytes())
		assert Ver(command, str), "Error: object received from controller was: " + str(command)
		_controllerevents[command]()

queues = {}

def flush():
	global proxies, queues
	
	for k in queues:
		cmdqueue = queues[k]
		proxyUp = proxies[k][0]
		
		proxyUp.send_bytes(Ser(" ".join(cmdqueue)))
		
		for command in cmdqueue:
			_servercmds[command](proxyUp)
	
	queues = {}

def doProxies():
	global proxies
	
	for proxyDown in map(lambda t: t[1], proxies.values()):
		while proxyDown.poll():
			commands = Des(proxyDown.recv_bytes())
			assert Ver(commands, str), "Error: object received from proxyDown was: " + str(command)
			
			for command in commands.split():
				_clientevents[command](proxyDown)

### Controller Radio Event Routines

def addproxy():
	global proxies, proxyGen
	proxies[next(proxyGen)] = G.SERVCONTDOWN.recv() # Receive a pipe to a proxy from the controller - this is a danger point since it uses pickling internally

def serverquit():
	G.ALIVE = False

_controllerevents = {
	"addproxy":	addproxy,
	"serverquit":	serverquit,
}

### Server Radio Commands

def dodraw(proxyUp):
	proxyUp.send_bytes(Ser(
		list(map(
			list,
			G.CONN.execute(Draw.drawQuery).fetchall()
		))
	))
	
	proxyUp.send_bytes(Ser(
		dict(map(
			lambda t: [t[0], t[1]], # Where 't[0]' is the RectID and 't[1]' is the rectangle
			R.RR.items(),
		))
	))

_servercmds = {
	"dodraw":	dodraw,
}

### Client Radio Event Routines

def getimages(proxyDown):
	proxyDown.send_bytes(Ser(
		dict(map(
			lambda t: [t[0], t[1]], # Where 't[0]' is the ImageID and 't[1]' is the pygame surface
			R.IR.items(),
		))
	))

def getbgd(proxyDown):
	proxyDown.send_bytes(Ser(Draw.bgd))

def getplayerid(proxyDown):
	proxyDown.send_bytes(Ser(Player.RectID))

_clientevents = {
	"getimages":	getimages,
	"getbgd":	getbgd,
	"getplayerid":	getplayerid,
}
