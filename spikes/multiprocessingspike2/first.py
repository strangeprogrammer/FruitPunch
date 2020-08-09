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

def main(fctlout, mfout, fsin):
	try:
		contflag = True
		while contflag:
			command = fctlout.recv()
			if command == "mode1":
				fctlout.send("ok")
				fsin.send(mfout.recv() * 10)
			elif command == "mode2":
				fctlout.send("ok")
				fsin.send(mfout.recv() * 100)
			elif command == "quit":
				fctlout.send("ok")
				contflag = False
			else:
				raise Exception("Command not found in process 'first'...")
	except BaseException as e:
		fctlout.send("notok")
