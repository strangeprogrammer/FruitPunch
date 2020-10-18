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

from ...Common import Time

from .. import G
from .. import Component as C

from . import Position

movingQuery = None

def init():
	global movingQuery
	
	movingQuery = sqa.select([
		C.VC.c.EntID,
		C.VC.c.VelX,
		C.VC.c.VelY,
	]).select_from(
		C.VC,
	).compile()

def quit():
	G.CONN.execute(
		C.VC.delete()
	)

def register(EntID):
	G.CONN.execute(
		C.VC.insert().values(EntID = EntID, VelX = 0, VelY = 0)
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.VC.select(C.VC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.VC.delete().where(C.VC.c.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa	.select([C.VC.c.VelX, C.VC.c.VelY]) \
			.select_from(C.VC) \
			.where(C.VC.c.EntID == EntID)
	).fetchone()

def store(EntID, VelX, VelY):
	G.CONN.execute(
		C.VC	.update() \
			.where(C.VC.c.EntID == EntID) \
			.values(VelX = VelX, VelY = VelY)
	)

def update():
	global movingQuery
	
	for EntID, VelX, VelY in G.CONN.execute(movingQuery).fetchall():
		(PosX, PosY) = Position.fetch(EntID)
		newX = PosX + VelX * Time.elapsed
		newY = PosY + VelY * Time.elapsed
		Position.store(EntID, newX, newY)
