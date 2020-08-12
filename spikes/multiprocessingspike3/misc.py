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

import sys

def strToBytes(s):
	return bytes(str(s), sys.getdefaultencoding())

def bytesToStr(byteobj):
	return str(byteobj, sys.getdefaultencoding())

def intToBytes(n):
	return strToBytes(int(n))

def bytesToInt(byteobj):
	return int(bytesToStr(byteobj))



def sendInt(pipe, n):
	return pipe.send_bytes(
		intToBytes(n)
	)

def sendStr(pipe, s):
	return pipe.send_bytes(
		strToBytes(s)
	)

def recvInt(pipe):
	return bytesToInt(
		pipe.recv_bytes()
	)

def recvStr(pipe):
	return bytesToStr(
		pipe.recv_bytes()
	)
