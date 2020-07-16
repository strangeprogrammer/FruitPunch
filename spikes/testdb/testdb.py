#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

# Import this file like:
#
# from testdb import ENGINE, DB, CONN, t1, t2
#
# And then you will have a simple database with which you can test your ideas.

import sqlalchemy as sqa
from sqlalchemy import (
	Table,
	Column,
	Integer,
	String,
	PrimaryKeyConstraint as PKC,
	ForeignKeyConstraint as FKC,
)

ENGINE = None
DB = None
CONN = None

t1 = None
t2 = None
t3 = None

def makeDB():
	global CONN, DB, ENGINE
	ENGINE = sqa.create_engine("sqlite:///:memory:")
	DB = sqa.MetaData()
	CONN = ENGINE.connect()

def makeTables():
	global CONN, DB, ENGINE, t1, t2, t3
	
	t1 = Table(
		"table1", DB,
		Column("Col1", Integer),
		Column("Col2", String),
		PKC("Col1"),
	)
	
	t2 = Table(
		"table2", DB,
		Column("Col2", String),
		Column("Col3", Integer),
		PKC("Col3"),
		FKC(["Col2"], ["table1.Col2"]),
	)
	
	t3 = Table(
		"table3", DB,
		Column("Col2", String),
		Column("Col3", Integer),
		PKC("Col3"),
		FKC(["Col2"], ["table1.Col2"]),
		FKC(["Col3"], ["table2.Col3"]),
	)
	
	DB.create_all(ENGINE)

def populateTables():
	global ENGINE, t1, t2, t3
	
	with ENGINE.connect() as CONN:
		CONN.execute(
			t1.insert(),
			[
				{"Col1": 5, "Col2": "hi"},
				{"Col1": 7, "Col2": "bye"},
			]
		)
		
		CONN.execute(
			t2.insert(),
			[
				{"Col2": "hi", "Col3": 6},
				{"Col2": "nope", "Col3": 2},
			]
		)
		
		CONN.execute(
			t3.insert(),
			[
				{"Col2": "nope", "Col3": 2},
				{"Col2": "eve", "Col3": 4},
			]
		)

def main():
	makeDB()
	makeTables()
	populateTables()
	print("Go nuts.")

main()
