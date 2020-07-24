#!/bin/sed -e 3q;d

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



from inspect import ismethod

from Backend import findTable

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
