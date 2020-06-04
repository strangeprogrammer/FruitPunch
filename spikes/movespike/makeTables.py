#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

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
