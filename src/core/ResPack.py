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



from . import G

class SyncDict(dict):
	def __init__(self, *args, getter = None, inserter = None, updater = None, deleter = None, **kwargs):
		super().__init__()
		self.getter = getter
		self.inserter = inserter
		self.updater = updater
		self.deleter = deleter
	
	def __getitem__(self, key):
		return self.getter(super(), key)
	
	def __setitem__(self, key, value):
		if key not in super().keys():
			self.inserter(key, value)
		elif super().__getitem__(key) != value: # Speed up by caching hash values?
			self.updater(key, value)
		
		super().__setitem__(key, value)
	
	def __delitem__(self, key):
		self.deleter(key)
		
		super().__delitem__(key)
	
	def invalidate(self, key):
		self.updater(key, super().__getitem__(key)) # Flush the value within the dictionary cache

class TaskQueue(list):
	def __init__(self, *args, runner = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.runner = runner
	
	def flush(self):
		for args in super().__iter__():
			self.runner(*args)
		
		self.clear()

class ResPack(SyncDict):
	def __init__(self, table, keyCol, packager):
		self.tq = TaskQueue(
			runner = G.CONN.execute
		)
		
		colname = keyCol.name
		
		self.sd = super().__init__(
			getter = lambda d, k:
				d.__getitem__(k),
			
			inserter = lambda k, v:
				self.tq.append([
					table.insert(),
					packager(k, v)
				]),
			
			updater = lambda k, v:
				self.tq.append([
					table.update().where(keyCol == k),
					packager(k, v)
				]),
			
			deleter = lambda k:
				self.tq.append([
					table.delete().where(keyCol == k)
				]),
		)
	
	def flush(self):
		with G.CONN.begin():
			self.tq.flush()
