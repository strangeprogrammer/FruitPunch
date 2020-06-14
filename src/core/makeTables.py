#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from sqlalchemy import (
	Table,
	Column,
	Integer,
	Boolean,
	REAL,
	PrimaryKeyConstraint as PKC,
	ForeignKeyConstraint as FKC,
	UniqueConstraint as UC,
)

from . import G

def makeTables():
	Table(	# List of all entity ID's
		"AllEnts", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
	)
	
	Table(	# List of all image ID's
		"AllImages", G.DB,
		Column("ImageID", Integer),
		PKC("ImageID"),
	)
	
	Table(	# List of all rectangle ID's
		"AllRects", G.DB,
		Column("RectID", Integer),
		PKC("RectID"),
	)
	
	Table(	# Entity-rectangle link table
		"RectComp", G.DB,
		Column("EntID", Integer),
		Column("RectID", Integer),
		PKC("EntID", "RectID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["RectID"], ["AllRects.RectID"]),
	)
	
	Table(	# Entity-image link table for the base image of an entity
		"ImageComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	Table(	# Entity-image link table for the renderable image of an entity
		"DrawComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
		FKC(["ImageID"], ["AllImages.ImageID"]),
	)
	
	Table(	# Real centers of all entities (useful for fine-grained velocity calculations)
		"PosComp", G.DB,
		Column("EntID", Integer),
		Column("PosX", REAL),
		Column("PosY", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	Table(	# Velocities of all entities
		"VelComp", G.DB,
		Column("EntID", Integer),
		Column("VelX", REAL),
		Column("VelY", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	Table(	# All player-controlled entities
		"PlayerComp", G.DB,
		Column("EntID", Integer),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	Table(	# All entities that have an image flip applied to them
		"FlipComp", G.DB,
		Column("EntID", Integer),
		Column("FlipX", Boolean),
		Column("FlipY", Boolean),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	Table(	# Images and their flipped equivalents
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
	
	Table(	# All entities that have an angle applied to them
		"RotationComp", G.DB,
		Column("EntID", Integer),
		Column("Theta", REAL),
		PKC("EntID"),
		FKC(["EntID"], ["AllEnts.EntID"]),
	)
	
	G.DB.create_all(G.ENGINE)
