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



import pygame as pg
import sqlalchemy as sqa
import math

from .. import G
from .. import Misc

exemptQuery = None
rotateQuery = None
collectable = []

from .. import Component as C
from .. import Resource as R

def init():
	global exemptQuery, rotateQuery
	
	exemptQuery = sqa.select([
		C.DC.c.EntID,
		C.DC.c.ImageID,
	]).select_from(
		C.DC
	).where(
		C.DC.c.EntID.notin_(
			sqa.select([C.ROTC.c.EntID]).select_from(C.ROTC)
		)
	).compile()
	
	rotateQuery = sqa.select([
		C.DC.c.EntID,
		C.DC.c.ImageID,
		C.ROTC.c.Theta,
	]).select_from(
		C.DC.join(C.ROTC, C.DC.c.EntID == C.ROTC.c.EntID)
	).compile()

def quit():
	G.CONN.execute(
		C.ROTC.delete()
	)
	
	collect()

def register(EntID):
	G.CONN.execute(
		C.ROTC.insert(), {
			"EntID": EntID,
			"Theta": 0,
		}
	)

def instances(EntID):
	return len(G.CONN.execute(
		C.ROTC.select(C.ROTC.c.EntID == EntID)
	).fetchall())

def deregister(EntID):
	G.CONN.execute(
		C.ROTC	.delete() \
			.where(C.ROTC.EntID == EntID)
	)

def fetch(EntID):
	return Misc.degToRad(
		G.CONN.execute(
			sqa	.select([C.ROTC.c.Theta]) \
				.select_from(C.ROTC) \
				.where(C.ROTC.c.EntID == EntID)
		).fetchone()[0]
	)

def store(EntID, Theta):
	G.CONN.execute(
		C.ROTC.update().where(
			C.ROTC.c.EntID == EntID
		), {
			"Theta": Misc.radToDeg(Theta)
		}
	)

def collect(): # We don't bother flushing 'R.IR' here since the data is so short-lived
	global collectable
	for rotateID in collectable:
		del R.IR[rotateID]
	
	collectable = []

def render(): # We don't bother flushing 'R.IR' here since the data is so short-lived
	global exemptQuery, rotateQuery, collectable
	
	result = G.CONN.execute(exemptQuery).fetchall()
	
	for EntID, ImageID, Theta in G.CONN.execute(rotateQuery).fetchall():
		rotateID = R.IR.append(
			pg.transform.rotate(R.IR[ImageID], Theta)
		)
		
		collectable.append(rotateID)
		
		result.append({
			"EntID": EntID,
			"ImageID": rotateID,
		})
	
	return result
