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



from sqlalchemy import (
	Table,
	Column,
	INTEGER,
	REAL,
	PrimaryKeyConstraint as PKC,
	ForeignKeyConstraint as FKC,
	UniqueConstraint as UC,
)

import G

def makeTables():
	Table(
		"AllEnts", G.DB,
		Column("EntID", INTEGER),
		PKC("EntID"),
	)
	
	Table(
		"AllImages", G.DB,
		Column("ImageID", INTEGER),
		PKC("ImageID"),
	)
	
	Table(
		"AllRects", G.DB,
		Column("RectID", INTEGER),
		PKC("RectID"),
	)
	
	Table(
		"RectComp", G.DB,
		Column("EntID", INTEGER),
		Column("RectID", INTEGER),
		PKC("EntID", "RectID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table(
		"ImageComp", G.DB,
		Column("EntID", INTEGER),
		Column("ImageID", INTEGER),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	Table(
		"RectCenterComp", G.DB,
		Column("RectID", INTEGER),
		Column("CenterX", REAL),
		Column("CenterY", REAL),
		PKC("RectID"),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table(
		"PlayerComp", G.DB,
		Column("EntID", INTEGER),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	G.DB.create_all(G.ENGINE)
