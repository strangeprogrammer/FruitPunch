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

from testModule import simpleFunc

DB = None
ENGINE = None

t1 = None

def makeDB():
	global DB, ENGINE
	ENGINE = sqa.create_engine("sqlite:///:memory:")
	DB = sqa.MetaData()

def loadTable():
	global DB, ENGINE
	
	# NEVER USE 'ENGINE.connect().connection.connection' AND NEVER DETACH THE CONNECTION, NEVER NEVER NEVER EVER!!!  SQLAlchemy BREAKS WHEN THIS HAPPENS!!!
	engineconn = ENGINE.raw_connection()
	
	file = open("./savefile.sql", "r")
	engineconn.cursor().executescript(file.read())
	file.close()
	
	engineconn.commit()
	engineconn.close()
	
	DB.reflect(bind = ENGINE)
	
	global t1
	t1 = DB.tables["table1"]

def printTable():
	global ENGINE, t1
	
	with ENGINE.connect() as CONN:
		results = CONN.execute(
			sqa.select([
				t1.c.Col1,
				t1.c.Col2,
				t1.c.Col3,
			])
		).fetchall()
		
		for [Col1, Col2, Col3] in results:
			print(Col1)
			print(Col2)
			print(pickle.loads(Col3))
			print("------------------")

def main():
	makeDB()
	loadTable()
	printTable()

main()
