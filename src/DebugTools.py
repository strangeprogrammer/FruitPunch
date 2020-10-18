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



from .Common import Time

from . import Config

class Sniffer():
	"""Wraps pipes and prints messages going through them along with an identifier string given during initialization."""
	
	def __init__(self, pipeish, procname):
		self.pipeish = pipeish
		self.procname = str(procname)
	
	def send_bytes(self, msg, *args, **kwargs):
		print("send: " + self.procname + ": " + str(msg))
		self.pipeish.send_bytes(msg, *args, **kwargs)
	
	def recv_bytes(self, *args, **kwargs):
		msg = self.pipeish.recv_bytes(*args, **kwargs)
		print("recv: " + self.procname + ": " + str(msg))
		return msg
	
	def __getattr__(self, name):
		return getattr(self.pipeish, name)

if Config.CONSOLEFPS:
	class FPSPrinter():
		"""Prints FPS information to the console at roughly regular intervals."""
		
		def __init__(self, interval, label = ""):
			self.interval = interval
			self.lastupdate = 0
			self.label = label
		
		def update(self):
			if self.lastupdate + self.interval < Time.now:
				self.lastupdate = (Time.now // self.interval) * self.interval
				print(self.label + str(Time._clock.get_fps()))
else:
	class FPSPrinter():
		def __init__(*args, **kwargs):	pass
		def update(*args, **kwargs):	pass
