#!/bin/python3

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



import pickle
import sqlalchemy as sqa
from sqlalchemy import (
	Table,
	Column,
	Integer,
	String,
	BLOB,
	PrimaryKeyConstraint as PKC,
)

from testModule import simpleFunc

DB = None
ENGINE = None

t1 = None

def makeDB():
	global DB, ENGINE
	ENGINE = sqa.create_engine("sqlite:///:memory:")
	DB = sqa.MetaData()

def makeTable():
	global DB, ENGINE, t1
	
	t1 = Table(
		"table1", DB,
		Column("Col1", Integer),
		Column("Col2", String),
		Column("Col3", BLOB),
		PKC("Col1"),
	)
	
	DB.create_all(ENGINE)

def populateTable():
	global ENGINE, t1
	
	with ENGINE.connect() as CONN:
		CONN.execute(
			t1.insert(), [
				{
					"Col1": 2356,
					"Col2": "lskjdxhf,v",
					"Col3": pickle.dumps({1, 5, 8}),
				}, {
					"Col1": 98765,
					"Col2": "wlekjrsfdg",
					"Col3": pickle.dumps(simpleFunc),
				},
			]
		)

def saveTable():
	global ENGINE
	
	with ENGINE.connect() as CONN:
		with open("./savefile.sql", "w") as file:
			contents = '\n'.join(CONN.connection.connection.iterdump())
			file.write(contents)

def main():
	makeDB()
	makeTable()
	populateTable()
	saveTable()

main()
