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



import json

from ..Common import SerDes

def DebugProxy(CLITOSERV):
	while True:
		raw = input().strip()
		commands = raw.split()
		
		if "quit" in commands:
			break
		
		CLITOSERV.send_bytes(SerDes.Ser(raw))
		
		for command in commands:
			if command == "echo":
				CLITOSERV.send_bytes(SerDes.Ser(input().strip()))
				response = SerDes.Des(CLITOSERV.recv_bytes())
				assert type(response) == str # TODO: Do something better than this
				print(response)
			elif command == "getdrawn":
				response = SerDes.Des(CLITOSERV.recv_bytes())
				assert type(response) == str # TODO: Do something better than this
				print(json.loads(response))
