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

def main(sctlout, fsout, smin):
	try:
		contflag = True
		while contflag:
			command = sctlout.recv()
			if command == "mode1":
				sctlout.send("ok")
				smin.send(fsout.recv() + 3)
			elif command == "mode2":
				sctlout.send("ok")
				smin.send(fsout.recv() + 6)
			elif command == "quit":
				sctlout.send("ok")
				contflag = False
			else:
				raise Exception("Command not found in process 'second'...")
	except BaseException as e:
		sctlout.send("notok")
