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



import multiprocessing as mp

from .Server import Server

from .Common.SerDes import (
	sendStr,
)

def main():
	startmethods = mp.get_all_start_methods()
	if "forkserver" in startmethods:
		startmethod = "forkserver"
	elif "fork" in startmethods:
		startmethod = "fork"
	else:
		startmethod = "spawn"
	mp.set_start_method(startmethod)
	
	[CONTTOSERV, SERVTOCONT] = mp.Pipe()
	
	ServerProc = mp.Process(target = Server.main, args = [SERVTOCONT])
	ServerProc.start()
	
	echoed = input()
	sendStr(CONTTOSERV, "echo")
	sendStr(CONTTOSERV, echoed)
	
	sendStr(CONTTOSERV, "quit")
	
	ServerProc.join()
