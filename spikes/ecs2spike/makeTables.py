#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

from sqlalchemy import (
	Table,
	Column,
	Integer,
	PrimaryKeyConstraint as PKC,
	ForeignKeyConstraint as FKC,
)

import G

def makeTables():
	Table(
		"AllEntities", G.DB,
		Column("EntID", Integer),
		PKC('EntID'),
	)
	
	Table(
		"ImageComp", G.DB,
		Column("EntID", Integer),
		Column("ImageID", Integer),
		PKC('EntID'),
		FKC(["EntID"], ["AllEntities.EntID"]),
	)
	
	Table(
		"RectComp", G.DB,
		Column("EntID", Integer),
		Column("RectID", Integer),
		PKC('EntID'),
		FKC(["EntID"], ["AllEntities.EntID"]),
	)
	
	G.DB.create_all(G.ENGINE)
