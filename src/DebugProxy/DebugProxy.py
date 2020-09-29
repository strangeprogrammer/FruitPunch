#!/bin/python3

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

from ..Common.ToBeGreen import (
	Ser,
	V,
	Ver,
	Des,
)

from ..Common import ExtraSerDes as ESD

def DebugProxy(CLITOSERV):
	ESD.init()
	
	while True:
		raw = input().strip()
		commands = raw.split()
		
		if "quit" in commands:
			break
		
		CLITOSERV.send_bytes(Ser(raw))
		
		for command in commands:
			if command == "echo":
				CLITOSERV.send_bytes(Ser(input().strip()))
				response = Des(CLITOSERV.recv_bytes())
				assert Ver(response, str), response
				print(response)
			elif command == "getdrawn":
				response = Des(CLITOSERV.recv_bytes())
				assert Ver(response, V.LIST(list)), response
				print(response)
			elif command == "getimages":
				response = Des(CLITOSERV.recv_bytes())
				assert Ver(response, V.LIST(V.PRODUCT(int, pg.Surface)))
				print(response)
			elif command == "getrects":
				response = Des(CLITOSERV.recv_bytes())
				assert Ver(response, V.LIST(
					V.PRODUCT(int, V.PRODUCT(
						int,
						int,
						int,
						int,
					))
				))
				print(response)
			else:
				raise Exception("Command input to DebugProxy was undefined...")
	
	ESD.quit()
