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

from .. import G

renderQuery = None

from .. import Component as C
from .. import Resource as R

def quit():
	G.CONN.execute(
		C.I.delete()
	)

def create(Filename, width = None, height = None):
	base = pg.image.load(
		Filename
	)#.convert_alpha()
	
	base_rect = base.get_rect()
	
	if width is not None and height is not None:
		base = pg.transform.scale(base, (width, height))
	elif width is not None and height is None:
		base = pg.transform.scale(base, (width, base_rect.height))
	elif width is None and height is not None:
		base = pg.transform.scale(base, (base_rect.width, height))
	
	base_rect = base.get_rect()
	width = base_rect.width
	height = base_rect.height
	
	ImageID = R.IR.append(base)
	
	G.CONN.execute(
		C.I.insert(), {
			"ImageID": ImageID,
			"Filename": Filename,
			"Width": width,
			"Height": height,
		}
	)
	
	return ImageID

def retrieve(ImageID):
	return G.CONN.execute(
		sqa.select([
			C.I.c.Filename,
			C.I.c.Width,
			C.I.c.Height,
		]).select_from(
			C.I
		).where(
			C.I.c.ImageID == ImageID
		)
	).fetchone()

def delete(ImageID):
	G.CONN.execute(
		C.I.delete().where(
			C.I.c.ImageID == ImageID
		)
	)
	
	del R.IR[ImageID]
