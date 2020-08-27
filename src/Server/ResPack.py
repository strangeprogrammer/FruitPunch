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

class InvalidatingMixin(dict):
	def invalidate(self, key):
		self.__setitem__(key, super().__getitem__(key)) # Forcefully flush a cache element
		if "invalidate" in super().__dict__:
			super().invalidate(key)

class CrudDict(InvalidatingMixin, dict):
	def __init__(self, *args, creator = None, retriever = None, updater = None, deleter = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.creator = creator
		self.retriever = retriever
		self.updater = updater
		self.deleter = deleter
	
	def __getitem__(self, key):
		return self.retriever(super(), key)
	
	def __setitem__(self, key, value):
		if key not in super().keys():
			self.creator(key, value)
		elif super().__getitem__(key) != value: # Speed up by caching hash values?
			self.updater(key, value)
		
		super().__setitem__(key, value)
	
	def __delitem__(self, key):
		self.deleter(key)
		
		super().__delitem__(key)

class TaskQueue(list):
	def __init__(self, *args, runner = None, **kwargs):
		super().__init__(*args, **kwargs)
		self.runner = runner
	
	def flush(self):
		for args in super().__iter__():
			self.runner(*args)
		
		self.clear()

class ResPack(CrudDict):
	def __init__(self, keyCol, packager):
		self.__tq = TaskQueue(
			runner = G.CONN.execute
		)
		
		table = keyCol.table
		colname = keyCol.name
		
		super().__init__(
			creator = lambda k, v:
				self.__tq.append([
					table.insert(),
					packager(k, v)
				]),
			
			retriever = lambda d, k:
				d.__getitem__(k),
			
			updater = lambda k, v:
				self.__tq.append([
					table.update().where(keyCol == k),
					packager(k, v)
				]),
			
			deleter = lambda k:
				self.__tq.append([
					table.delete().where(keyCol == k)
				]),
		)
	
	def flush(self):
		with G.CONN.begin():
			self.__tq.flush()
