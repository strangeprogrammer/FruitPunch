#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from inspect import ismethod

allResources = {}

def create(resName):
	global allResources
	allResources[resName] = {}

def retrieve(resName):
	global allResources
	return allResources[resName]

def delete(resName):
	global allResources
	del allResources[resName]

def require(requirement):
	"""
	Called like:
	
	@...
	@Resource.require("Res2")
	@Resource.require("Res1")
	def update(self, dict1, dict2, ...):
	
	Or:
	
	@...
	@Resource.require("Res2")
	@Resource.require("Res1")
	def update(dict1, dict2, ...):
	
	NOTE: Performs the resource lookup each time the function is called.
	"""
	
	def decorator(f):
		# Change the wrapper depending upon whether or not 'f' is a method
		if ismethod(f):
			def wrapper(self, *args, **kwargs):
				return self.f(retrieve(requirement), *args, **kwargs)
		else:
			def wrapper(*args, **kwargs):
				return f(retrieve(requirement), *args, **kwargs)
		
		return wrapper
	
	return decorator
