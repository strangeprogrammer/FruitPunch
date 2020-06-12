#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from inspect import ismethod

import sqlalchemy as sqa

from . import G

def DBInit():
	G.ENGINE = sqa.create_engine("sqlite:///:memory:")
	G.DB = sqa.MetaData()
	G.CONN = G.ENGINE.connect()

def findTable(tableName):
	for table in G.DB.sorted_tables:
		if table.name == tableName:
			return table
	
	return None

def require(requirement):
	"""
	Called like:
	
	@...
	@Component.require("Comp2")
	@Component.require("Comp1")
	def update(self, table1, table2, ...):
	
	Or:
	
	@...
	@Component.require("Comp2")
	@Component.require("Comp1")
	def update(table1, table2, ...):
	
	NOTE: Performs the table lookup each time the function is called.
	"""
	
	def decorator(f):
		# Change the wrapper depending upon whether or not 'f' is a method
		if ismethod(f):
			def wrapper(self, *args, **kwargs):
				return self.f(findTable(requirement), *args, **kwargs)
		else:
			def wrapper(*args, **kwargs):
				return f(findTable(requirement), *args, **kwargs)
		
		return wrapper
	
	return decorator
