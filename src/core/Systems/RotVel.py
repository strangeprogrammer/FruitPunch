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



import sqlalchemy as sqa
import math

from .. import G
from .. import Misc
from .. import Time

from .. import Component as C

from . import Rotation

rotateQuery = None

def init():
	global rotateQuery
	
	rotateQuery = sqa.select([
		C.RVC.c.EntID,
		C.RVC.c.Omega,
	]).select_from(
		C.RVC
	).compile()

def quit():
	G.CONN.execute(
		C.RVC.delete()
	)

def register(EntID):
	G.CONN.execute(
		C.RVC.insert(), {
			"EntID": EntID,
			"Omega": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.RVC.select().where(C.RVC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.RVC.delete().where(C.RVC.c.EntID == EntID)
	)

def fetch(EntID):
	return Misc.degToRad(
		G.CONN.execute(
			sqa	.select([C.RVC.c.Omega]) \
				.select_from(C.RVC) \
				.where(C.RVC.c.EntID == EntID)
		).fetchone()[0]
	)

def store(EntID, Omega):
	G.CONN.execute(
		C.RVC.update().where(C.RVC.c.EntID == EntID), {
			"Omega": Misc.radToDeg(Omega),
		}
	)

def update():
	global rotateQuery
	
	for EntID, Omega in G.CONN.execute(rotateQuery).fetchall():
		Theta = Rotation.fetch(EntID)
		newTheta = Theta + Misc.degToRad(Omega) * Time.elapsed
		Rotation.store(EntID, newTheta)
