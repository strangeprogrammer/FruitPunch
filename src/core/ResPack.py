#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from itertools import count

from . import G

class ResPack(dict):
	def __init__(self, *args, table = None, field = None, **kwargs):
		super().__init__()
		
		self.table = table
		self.field = field
		self.counter = count()
	
	def append(self, value):
		index = next(self.counter)
		self[index] = value
		return index
	
	def __setitem__(self, key, value):
		if self.table is not None and key not in self:
			G.CONN.execute(
				self.table.insert(), {
					self.field: key
				}
			)
		
		super().__setitem__(key, value)
	
	def __delitem__(self, key):
		if self.table is not None:
			G.CONN.execute(
				self.table.delete().where(
					getattr(self.table.columns, self.field) == key
				)
			)
		
		super().__delitem__(key)
