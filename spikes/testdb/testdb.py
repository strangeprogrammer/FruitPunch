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



# Import this file like:
#
# from testdb import ENGINE, DB, t1, t2, t3
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

t1 = None
t2 = None
t3 = None

def makeDB():
	global DB, ENGINE
	ENGINE = sqa.create_engine("sqlite:///:memory:")
	DB = sqa.MetaData()

def makeTables():
	global DB, ENGINE, t1, t2, t3
	
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
