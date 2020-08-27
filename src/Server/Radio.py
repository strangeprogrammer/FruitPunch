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



from . import G

from ..Common.SerDes import (
	serialize,
	deserialize,
)

proxies = []

def doController():
	while G.SERVTOCONT.poll():
		command = deserialize(G.SERVTOCONT.recv_bytes())
		assert type(command) == str # TODO: Replace this with something cleaner
		
		if command == "addproxy":
			global proxies
			proxies.append(G.SERVTOCONT.recv()) # Receive a pipe to a proxy from the controller - this is a danger point since it uses pickling internally
		elif command == "quit":
			G.ALIVE = False
		else:
			raise Exception("Command received from controller was undefined...")

def doProxies():
	global proxies
	for proxy in proxies:
		while proxy.poll():
			command = deserialize(proxy.recv_bytes())
			assert type(command) == str # TODO: Replace this with something cleaner
			
			if command == "echo":
				response = deserialize(proxy.recv_bytes())
				assert type(response) == str # TODO: Replace this with something cleaner
				proxy.send_bytes(serialize(response))
			else:
				raise Exception("Command received from proxy was undefined...")

def update():
	doController()
	doProxies()
