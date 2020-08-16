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
from sqlalchemy import (
	Table,
	Column,
	Integer,
	Boolean,
	REAL,
	String,
	PrimaryKeyConstraint as PKC,
	ForeignKeyConstraint as FKC,
	UniqueConstraint as UC,
	Index,
)

from . import G

E = I = R = RECC = IC = DC = LC = POSC = ROTC = VC = RVC = AC = FC = FI = FDC = RDC = SBC = SC = CT = CU = None

def init():
	G.ENGINE = sqa.create_engine("sqlite:///:memory:")
	G.DB = sqa.MetaData()
	G.CONN = G.ENGINE.connect()
	
	global E, I, R, RECC, IC, DC, LC, POSC, ROTC, VC, RVC, AC, FC, FI, FDC, RDC, SBC, SC, CT, CU
	
	E = Table( # List of all entity ID's
		"AllEnts", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
	)
	
	I = Table( # List of all image ID's and information used to generate them
		"AllImages", G.DB,
		Column("ImageID", Integer),
		Column("Filename", String),
		Column("Width", Integer),
		Column("Height", Integer),
		PKC("ImageID"),
	)
	
	R = Table( # List of all rectangle ID's
		"AllRects", G.DB,
		Column("RectID", Integer),
		PKC("RectID"),
	)
	
	RECC = Table( # Entity-rectangle link table
		"RectComp", G.DB,
		Column("EntID", Integer),
		Column("RectID", Integer),
		PKC("EntID", "RectID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	IC = Table( # Entity-image link table for the base image of an entity
		"ImageComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	DC = Table( # Entity-image link table for the renderable image of an entity
		"DrawComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	LC = Table( # Drawing layer information for all entities
		"LayerComp", G.DB,
		Column("EntID", Integer),
		Column("Major", Integer),	# Anti-functional dependency:
		Column("SubMajor", Integer),	# If 2 tuples have the same Major number, they must NOT have the same SubMajor number
		Column("Minor", Integer),	# (Similarly for SubMajor and Minor number)
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		Index("IDX_Layer", "Major", "SubMajor", "Minor"),
	)
	
	POSC = Table( # Real centers of all entities (useful for fine-grained velocity calculations)
		"PosComp", G.DB,
		Column("EntID", Integer),
		Column("PosX", REAL),
		Column("PosY", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	ROTC = Table( # Entities that have an angle applied to them
		"RotationComp", G.DB,
		Column("EntID", Integer),
		Column("Theta", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	VC = Table( # Velocities of all entities
		"VelComp", G.DB,
		Column("EntID", Integer),
		Column("VelX", REAL),
		Column("VelY", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	RVC = Table( # Angular velocities of all entities
		"RotVelComp", G.DB,
		Column("EntID", Integer),
		Column("Omega", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	AC = Table( # Velocities of all entities
		"AccelComp", G.DB,
		Column("EntID", Integer),
		Column("AccX", REAL),
		Column("AccY", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	FC = Table( # Entities that have an image flip applied to them
		"FlipComp", G.DB,
		Column("EntID", Integer),
		Column("FlipX", Boolean),
		Column("FlipY", Boolean),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	FI = Table( # Images and their flipped equivalents
		"FlipImages", G.DB,
		Column("InImageID", Integer),
		Column("FlipX", Boolean),
		Column("FlipY", Boolean),
		Column("OutImageID", Integer),
		PKC("InImageID", "FlipX", "FlipY"),
		UC("OutImageID"),
		FKC(["InImageID"], ["AllImages.ImageID"]),
		FKC(["OutImageID"], ["AllImages.ImageID"]),
	)
	
	FDC = Table( # Entities that use the flip state of the parent to determine their own flip state
		"FlipDollComp", G.DB,
		Column("EntID", Integer),
		Column("ChildID", Integer),
#		Column("Generation", Integer),
		Column("OffX", Boolean),
		Column("OffY", Boolean),
		PKC("ChildID"),
		FKC(["ChildID"], ["AllEnts.EntID"]),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	RDC = Table( # Entities that have an angle applied to them
		"RotDollComp", G.DB,
		Column("EntID", Integer),
		Column("ChildID", Integer),
		Column("dTheta", REAL),
		PKC("ChildID"),
		FKC(["ChildID"], ["AllEnts.EntID"]),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	SBC = Table( # Base strut offsets of all affected entities
		"StrutBaseComp", G.DB,
		Column("EntID", Integer),
		Column("ChildID", Integer),
		Column("OffX", REAL),
		Column("OffY", REAL),
		PKC("ChildID"),
		FKC(["ChildID"], ["AllEnts.EntID"]),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	SC = Table( # Strut offsets of all affected entities
		"StrutComp", G.DB,
		Column("EntID", Integer),
		Column("ChildID", Integer),
		Column("OffX", REAL),
		Column("OffY", REAL),
		PKC("ChildID"),
		FKC(["ChildID"], ["AllEnts.EntID"]),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	CT = Table( # All entities that can collide with other entities and perform an action when they do
		"CollTrigg", G.DB,
		Column("EntID", Integer),
		Column("OnColl", Integer),
		Column("OffColl", Integer),
		PKC("EntID", "OnColl", "OffColl"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	CU = Table( # All entities that can collide with other entities and trigger the other's collision actions
		"CollUnTrigg", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	G.DB.create_all(G.ENGINE)

def quit():
	G.CONN.close()
	
	G.ENGINE = None
	G.DB = None
	G.CONN = None

def retrieve(compName):
	for table in G.DB.sorted_tables:
		if table.name == compName:
			return table
	
	return None # Perhaps throw an exception instead
