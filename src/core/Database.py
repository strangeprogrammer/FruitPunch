#!/bin/sed -e 3q;d;

# DO NOT RUN THIS FILE - import it instead

from functools import partial
from sys import modules
import sqlalchemy as sqa

from . import G

def init():
	G.ENGINE = sqa.create_engine("sqlite:///:memory:")
	G.DB = sqa.MetaData()
	G.CONN = G.ENGINE.connect()
