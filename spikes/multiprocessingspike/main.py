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

import first
import second

def main():
	mp.set_start_method('fork')
	
	[mfin, mfout] = mp.Pipe()
	[fsin, fsout] = mp.Pipe()
	[smin, smout] = mp.Pipe()
	
	f = mp.Process(target = first.main, args = (mfout, fsin))
	s = mp.Process(target = second.main, args = (fsout, smin))
	
	f.start()
	s.start()
	
	mfin.send(int(input("NUMBER> ") or 0))
	
	f.join()
	s.join()
	
	print(smout.recv())
	
	mfin.close()
	smout.close()

main()
