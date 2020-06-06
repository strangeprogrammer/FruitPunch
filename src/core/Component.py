#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from inspect import ismethod

from .Backend import findTable

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
