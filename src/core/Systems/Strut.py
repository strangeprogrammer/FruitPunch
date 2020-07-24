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

updateQuery = None

from .. import Component as C

def init():
	global updateQuery
	
	updateQuery = sqa.select([
		C.SBC.c.ChildID,
		C.POSC.c.PosX,
		C.POSC.c.PosY,
		C.SBC.c.OffX,
		C.SBC.c.OffY,
	]).select_from(
		C.POSC.join(C.SBC, C.POSC.c.EntID == C.SBC.c.EntID)
	).compile()

def quit():
	G.CONN.execute(
		C.SBC.delete()
	)

def register(EntID, ChildID):
	G.CONN.execute(
		C.SBC.insert(), {
			"EntID": EntID,
			"ChildID": ChildID,
			"OffX": 0,
			"OffY": 0,
		}
	)

def instances(ChildID):
	return len(G.CONN.execute(
		C.SBC.select().where(C.SBC.c.ChildID == ChildID)
	).fetchall())

def deregister(ChildID):
	G.CONN.execute(
		C.SBC.delete().where(C.SBC.c.ChildID == ChildID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.SBC.c.OffX, C.SBC.c.OffY]) \
			.select_from(C.SBC) \
			.where(C.SBC.c.ChildID == ChildID)
	).fetchone()

def store(ChildID, OffX, OffY):
	G.CONN.execute(
		C.SBC.update().where(
			C.SBC.c.ChildID == ChildID,
		), {
			"OffX": OffX,
			"OffY": OffY,
		}
	)

def _updateStrutComp(values):
	G.CONN.execute(C.SC.delete())
	if 0 < len(values):
		G.CONN.execute(C.SC.insert(), values)

def _resetStrutComp():
	_updateStrutComp(
		G.CONN.execute(
			C.SBC.select()
		).fetchall()
	)

def update():
	_resetStrutComp()
	
	global updateQuery
	for ChildID, PosX, PosY, OffX, OffY in G.CONN.execute(updateQuery).fetchall():
		G.CONN.execute(
			C.POSC.update().where(C.POSC.c.EntID == ChildID), {
				"PosX": PosX + OffX,
				"PosY": PosY + OffY,
			}
		)
