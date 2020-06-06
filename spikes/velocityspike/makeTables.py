#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from sqlalchemy import (
	Table,
	Column,
	Integer,
	REAL,
	PrimaryKeyConstraint as PKC,
	ForeignKeyConstraint as FKC,
	UniqueConstraint as UC,
)

import G

def makeTables():
	Table(
		"AllEnts", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
	)
	
	Table(
		"AllImages", G.DB,
		Column("ImageID", Integer),
		PKC("ImageID"),
	)
	
	Table(
		"AllRects", G.DB,
		Column("RectID", Integer),
		PKC("RectID"),
	)
	
	Table(
		"AllMove", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	Table(
		"RectComp", G.DB,
		Column("EntID", Integer),
		Column("RectID", Integer),
		PKC("EntID", "RectID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table(
		"ImageComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	Table(
		"PositionComp", G.DB,
		Column("RectID", Integer),
		Column("PosX", REAL),
		Column("PosY", REAL),
		PKC("RectID"),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table(
		"VelocityComp", G.DB,
		Column("RectID", Integer),
		Column("VelX", REAL),
		Column("VelY", REAL),
		PKC("RectID"),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table(
		"PlayerComp", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	G.DB.create_all(G.ENGINE)
