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



import pygame as pg
import sqlalchemy as sqa

from . import (
	G,
	Component,
	Component as C,
	Resource,
	Time,
	PlayerMove,
	CollHandLib,
	LevelLoader,
)

from .Systems import (
	Camera,
	Draw,
	Flip,
	Position,
	Rotation,
	Velocity,
	RotVel,
	Accel,
	FlipDoll,
	RotDoll,
	Strut,
	Collision,
	Layer,
	ImageLoader,
)

def load(fileName):
	Component.init()
	Resource.init()
	
	Flip.init()
	
	Position.init()
	Rotation.init()
	Velocity.init()
	RotVel.init()
	Accel.init()
	
	FlipDoll.init()
	RotDoll.init()
	Strut.init()
	
	Collision.init()
	
#	Camera.init()
	
	Draw.init()
	
#	PlayerMove.init()
	
	CollHandLib.init()
	
	Time.init()
	
	
	
	Draw.bgd = LevelLoader.load(fileName)
	
#	Camera.bind(
#		G.CONN.execute(
#			sqa	.select([C.PLYC.c.EntID]) \
#				.select_from(C.PLYC)
#		).scalar()
#	)
	
#	Camera.update()

def unload():
	CollHandLib.quit()
	
#	PlayerMove.quit()
	
	Draw.quit()
	
#	Camera.quit()
	
	Collision.quit()
	
	Strut.quit()
	RotDoll.quit()
	FlipDoll.quit()
	
	Accel.quit()
	RotVel.quit()
	Velocity.quit()
	Rotation.quit()
	Position.quit()
	
	Flip.quit()
	
	Layer.quit()
	
	ImageLoader.quit()
	
	Resource.quit()
	Component.quit()
