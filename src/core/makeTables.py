#!/bin/sed -e 3q;d;

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

from . import G

def makeTables():
	Table( # List of all entity ID's
		"AllEnts", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
	)
	
	Table( # List of all image ID's
		"AllImages", G.DB,
		Column("ImageID", Integer),
		PKC("ImageID"),
	)
	
	Table( # List of all rectangle ID's
		"AllRects", G.DB,
		Column("RectID", Integer),
		PKC("RectID"),
	)
	
	Table( # List of all moving objects
		"AllMove", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	Table( # Entity-rectangle link table
		"RectComp", G.DB,
		Column("EntID", Integer),
		Column("RectID", Integer),
		PKC("EntID", "RectID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table( # Entity-image link table for the base image of an entity
		"ImageComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	Table( # Entity-image link table for the renderable image of an entity
		"DrawComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	Table( # Real centers of all rectangles (useful for fine-grained velocity calculations)
		"PositionComp", G.DB,
		Column("RectID", Integer),
		Column("PosX", REAL),
		Column("PosY", REAL),
		PKC("RectID"),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table( # Velocities of all rectangels
		"VelocityComp", G.DB,
		Column("RectID", Integer),
		Column("VelX", REAL),
		Column("VelY", REAL),
		PKC("RectID"),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table( # All player-controlled entities
		"PlayerComp", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	G.DB.create_all(G.ENGINE)
