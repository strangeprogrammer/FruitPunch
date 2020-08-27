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



### Backend Functions

def strToBytes(s):
	return bytes(str(s), "utf-8")

def bytesToStr(byteobj):
	return str(byteobj, "utf-8")

def getmeasures(bobj):
	datastart = bobj.index(b" ") + 1 # NOTE: The constant '1' is the size of the b" "
	blength = int(
		bytesToStr(
			bobj[ : datastart - 1]
		)
	)
	return [datastart, blength]

def cap(bobj, n):
	return strToBytes(str(n)) + b" " + bobj

def pascalify(bobj):
	return cap(bobj, len(bobj))

def uncap(bobj):
	[datastart, blength] = getmeasures(bobj)
	return [blength, bobj[datastart : ]]

def peel(bobj):
	[datastart, blength] = getmeasures(bobj)
	return [
		bobj[datastart : datastart + blength],	# What we expect to receive given 'blength'
		bobj[datastart + blength : ],		# What we didn't expect to receive
	]

### Front-end Functions

def serialize(x): # Serialize
	if type(x) == str:
		return pascalify(b"str") + pascalify(strToBytes(x))
	elif type(x) == int:
		return pascalify(b"int") + pascalify(strToBytes(x))
	elif type(x) == list:
		bobj = b""
		for y in x:
			bobj += pascalify(serialize(y))
		return pascalify(b"list") + cap(bobj, len(x))
	else:
		raise Exception("Couldn't serialize object: " + repr(x))

def deserialize(bobj): # Deserialize
	[t, bobj] = peel(bobj)
	if t == b"str":
		return bytesToStr(peel(bobj)[0])
	elif t == b"int":
		return int(bytesToStr(peel(bobj)[0]))
	elif t == b"list":
		x = []
		[numelems, bobj] = uncap(bobj)
		while 0 < numelems:
			[y, bobj] = peel(bobj)
			x.append(deserialize(y))
			numelems -= 1
		return x
	else:
		raise Exception("Couldn't deserialize object: " + repr(bobj))
