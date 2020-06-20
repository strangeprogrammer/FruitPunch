#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from functools import partial
from sys import modules
from itertools import count

allResources = {}

class ResPack():
	def __init__(self):
		self.members = {}
		
		self.counter = count()
	
	def append(self, value):
		index = next(self.counter)
		self.members[index] = value
		return index
	
	def __getitem__(self, key):
		return self.members[key]
	
	def __setitem__(self, key, value):
		self.members[key] = value
	
	def __delitem__(self, key):
		del self.members[key]

def create(resName):
	global allResources
	allResources[resName] = ResPack()
	return allResources[resName]

def retrieve(resName):
	global allResources
	return allResources[resName]

def delete(resName):
	global allResources
	del allResources[resName]
