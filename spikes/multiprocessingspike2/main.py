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

def pipeack(commpipe, data):
	commpipe.send(data)
	if commpipe.recv() != "ok":
		raise Exception("A child process didn't operate correctly...")

def main():
	mp.set_start_method('fork')
	
	[fctlin, fctlout] = mp.Pipe()
	[sctlin, sctlout] = mp.Pipe()
	[mfin, mfout] = mp.Pipe()
	[fsin, fsout] = mp.Pipe()
	[smin, smout] = mp.Pipe()
	
	f = mp.Process(target = first.main, args = (fctlout, mfout, fsin))
	s = mp.Process(target = second.main, args = (sctlout, fsout, smin))
	
	try:
		f.start()
		s.start()
		
		for [fmode, smode] in [
			["mode1", "mode1"],
			["mode2", "mode1"],
			["mode1", "mode2"],
			["mode2", "mode2"],
		]:
			pipeack(fctlin, fmode)
			pipeack(sctlin, smode)
			mfin.send(int(input("NUMBER> ") or 0))
			print(smout.recv())
		
		pipeack(fctlin, "quit")
		pipeack(sctlin, "quit")
		
		f.join()
		s.join()
	except Exception as e:
		f.terminate()
		s.terminate()
		
		raise e

main()
