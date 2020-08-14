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

from misc import (
	sendStr,
	recvStr,
)

import link

def main():
	[linkctlin, linkctlout] = mp.Pipe()
	linkProc = mp.Process(target = link.main, args = [linkctlout])
	linkProc = mp.Process(target = link.main, args = [linkctlout])
	
	linkProc.start()
	
	sendStr(linkctlin, "nopasspipe")
	
	for message in [
		"Hello, world!",
		"Planetarium!",
		"Krusty Krab is unfair!",
	]:
		[toClient, toServer] = mp.Pipe()
		
		sendStr(linkctlin, "passpipe")
		linkctlin.send(toServer)
		sendStr(toClient, message)
	
	sendStr(linkctlin, "quit")
	
	linkProc.join()

main()
