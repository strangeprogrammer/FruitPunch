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



import multiprocessing as mp

from Misc import getUpdates
import mirror

def main():
	mp.set_start_method("spawn")
	
	[MAINTOMIRROR, MIRRORTOMAIN] = mp.Pipe()
	
	mirrorProc = mp.Process(target = mirror.main, args = [MIRRORTOMAIN])
	mirrorProc.start()
	
	
	
	oldDict = {
		"first": "1",
		"second": "2",
		"third": "3",
	}
	MAINTOMIRROR.send(oldDict)
	
	try:
		command = input("command > ")
		while command != "quit":
			if command == "set":
				updates = {
					input("key >   "):
					input("value > "),
				}
				newDict = {**oldDict, **updates}
				
				MAINTOMIRROR.send("update")
				MAINTOMIRROR.send(getUpdates(oldDict, newDict))
				oldDict = newDict
			elif command == "del":
				k = input("key >   ")
				newDict = oldDict.copy()
				del newDict[k]
				
				MAINTOMIRROR.send("update")
				MAINTOMIRROR.send(getUpdates(oldDict, newDict))
				oldDict = newDict
			elif command == "get":
				MAINTOMIRROR.send("print")
				MAINTOMIRROR.recv()
			else:
				raise Exception("Command received from user not found...")
			
			command = input("command > ")
		
		MAINTOMIRROR.send("quit")
	except Exception as e:
		print(e)
		mirrorProc.terminate()
	
	
	
	mirrorProc.join()

if __name__ == "__main__":
	main()
