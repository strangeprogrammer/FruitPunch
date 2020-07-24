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

from .. import G

rectPosQuery = None

from .. import Component as C
from .. import Resource as R

def init():
	global rectPosQuery
	
	rectPosQuery = sqa.select([
		C.RECC.c.RectID,
		C.POSC.c.PosX,
		C.POSC.c.PosY,
	]).select_from(
		C.RECC.join(C.POSC, C.RECC.c.EntID == C.POSC.c.EntID)
	).compile()

def quit():
	G.CONN.execute(
		C.POSC.delete()
	)

def register(EntID):
	G.CONN.execute(
		C.POSC.insert(), {
			"EntID": EntID,
			"PosX": 0,
			"PosY": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.POSC.select().where(C.POSC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.POSC.delete().where(C.POSC.c.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.POSC.c.PosX, C.POSC.c.PosY]) \
			.select_from(C.POSC) \
			.where(C.POSC.c.EntID == EntID)
	).fetchone()

def store(EntID, PosX, PosY):
	G.CONN.execute(
		C.POSC	.update() \
			.where(C.POSC.c.EntID == EntID), {
			"PosX": PosX,
			"PosY": PosY,
		}
	)

def update():
	global rectPosQuery
	
	for RectID, PosX, PosY in G.CONN.execute(rectPosQuery).fetchall():
		oldcenter = R.RR[RectID].center
		if oldcenter != (PosX, PosY):
			R.RR[RectID].center = (PosX, PosY)
			R.RR.invalidate(RectID)
	
	R.RR.flush()
