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

proxies = []
proxyGen = count()

def doController():
	while G.SERVTOCONT.poll():
		command = Des(G.SERVTOCONT.recv_bytes())
		assert Ver(command, str)
		
		if command == "addproxy":
			global proxies, proxyGen
			proxies.append([
				G.SERVTOCONT.recv(), # Receive a pipe to a proxy from the controller - this is a danger point since it uses pickling internally
				next(proxyGen),
			])
		elif command == "quit":
			G.ALIVE = False
		else:
			raise Exception("Command received from controller was undefined...")

def doProxies():
	global proxies
	for [proxy, proxyID] in proxies:
		while proxy.poll():
			commands = Des(proxy.recv_bytes())
			assert Ver(commands, str)
			
			for command in commands.split():
				if command == "getdrawn":
					proxy.send_bytes(Ser(
						list(map(
							lambda x: [x["RectID"], x["ImageID"], x["Major"], x["SubMajor"], x["Minor"]],
							G.CONN.execute(Draw.drawQuery).fetchall()
						))
					))
				elif command == "getimages":
					proxy.send_bytes(Ser(
						dict(map(
							lambda t: [t[0], t[1]], # Where 't[0]' is the ImageID and 't[1]' is the pygame surface
							R.IR.items(),
						))
					))
				elif command == "getrects":
					proxy.send_bytes(Ser(
						dict(map(
							lambda t: [t[0], t[1]], # Where 't[0]' is the RectID and 't[1]' is the rectangle
							R.RR.items(),
						))
					))
				elif command == "getbgd":
					proxy.send_bytes(Ser(Draw.bgd))
				elif command == "getplayerid":
					proxy.send_bytes(Ser(Player.RectID))
				else:
					raise Exception("Command received from proxy was undefined...")
