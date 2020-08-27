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



from .ResPack import ResPack
from .Misc import incrementable

from . import Component as C

ER = IR = RR = CR = CCR = AAR = None

def init():
	global ER, IR, RR, CR, CCR, AAR
	
	class Dict(dict): # https://stackoverflow.com/a/2827664
		pass
	
	ER = incrementable(ResPack( # Entity Resource
		keyCol = C.E.c.EntID,
		packager = lambda k, v: { # This is only an example for now
			"EntID": k
		}
	))
	
	IR	= incrementable(Dict())
	
	RR = incrementable(ResPack( # Rectangle Resource
		keyCol = C.R.c.RectID,
		packager = lambda k, v: { # This is only an example for now
			"RectID": k
		}
	))
	
	CR	= incrementable(Dict()) # Collision Resource
	CCR	= incrementable(Dict()) # Continuous Collision Resource
	AAR	= incrementable(Dict()) # Auxilliary Attribute Resource

def quit():
	global ER, IR, RR, CR, CCR, AAR
	ER = IR = RR = CR = CCR = AAR = None
