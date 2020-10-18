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

import sys
import marshal

def customkey(t):
	[filename, lineno, funcname, primcalls, totcalls, tottime, cumtime, callers] = t
	return tottime

def main():
	if len(sys.argv) != 3:
		return 1
	
	with open(sys.argv[1], "rb") as fin:
		with open(sys.argv[2], "w") as fout:
			print(
				"%22s %85s %15s %60s %20s %15s %22s %22s" % (
					"Key",
					"Filename",
					"Line Number",
					"Function Name",
					"Primitive Calls",
					"Total Calls",
					"Total Time",
					"Cumulative Time",
				),
				file = fout
			)
			
			for item in sorted(
				map( # Convert silly dictionary into list
					lambda t: list(t[0]) + list(t[1]),
					marshal.load(fin).items()
				),
				key = customkey,
				reverse = True,
			):
				print(
					"%22f %85s %15i %60s %20i %15i %22f %22f" % (customkey(item), *item[:-1]),
					file = fout
				)
	
	return 0

main()
