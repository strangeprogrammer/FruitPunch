#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import sqlalchemy as sqa

from . import G

def DBInit():
	G.ENGINE = sqa.create_engine("sqlite:///")
	G.DB = sqa.MetaData()
	G.CONN = G.ENGINE.connect()

def findTable(tableName):
	for table in G.DB.sorted_tables:
		if table.name == tableName:
			return table
	
	return None
