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

from misc import (
	bytesToStr,
	sendInt,
	sendStr,
	recvInt,
	recvStr,
)

def main(fctlout, mfout, fsin):
	try:
		command = recvStr(fctlout)
		while not command == "quit":
			if command == "mode1":
				sendInt(fsin, recvInt(mfout) * 10)
			elif command == "mode2":
				sendInt(fsin, recvInt(mfout) * 100)
			else:
				raise Exception("Command '" + bytesToStr(command) + "' not found in process 'first'...")
			
			command = recvStr(fctlout)
	except BaseException as e:
		sendStr(fctlout, "notok")
