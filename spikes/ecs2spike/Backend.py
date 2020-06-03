#!/bin/sed -e 3q;d

# DO NOT RUN THIS FILE - import it instead

import G

def findTable(tableName):
	for table in G.DB.sorted_tables:
		if table.name == tableName:
			return table
	
	return None
