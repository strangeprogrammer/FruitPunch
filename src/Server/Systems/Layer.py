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

from .. import Component as C

def quit():
	G.CONN.execute(
		C.LC.delete()
	)

def register(EntID):
	G.CONN.execute(
		C.LC.insert(), {
			"EntID": EntID,
			"Major": -1,
			"SubMajor": -1,
			"Minor": -1,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.LC.select(C.LC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.LC.delete().where(C.LC.c.EntID == EntID)
	)

def fetch(EntID):
	return G.CONN.execute(
		sqa.select([
			C.LC.c.Major,
			C.LC.c.SubMajor,
			C.LC.c.Minor,
		]).select_from(
			C.LC
		).where(
			C.LC.c.EntID == EntID
		)
	).fetchone()[0]

def store(EntID, Major, SubMajor = -1, Minor = -1):
	G.CONN.execute(
		C.LC	.update() \
			.where(C.LC.c.EntID == EntID), {
			"Major": Major,
			"SubMajor": SubMajor,
			"Minor": Minor,
		}
	)
