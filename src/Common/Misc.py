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



import itertools
import math
import pygame as pg

def radToDeg(theta):
	return theta * 360 / math.tau

def degToRad(theta):
	return theta * math.tau / 360

class Rect(pg.Rect):
	def __add__(self, other):
		return Rect(
			self.left + other.left,
			self.top + other.top,
			self.width,
			self.height,
		)
	
	def __sub__(self, other):
		return Rect(
			self.left - other.left,
			self.top - other.top,
			self.width,
			self.height,
		)
	
	def isValid(self):
		return 0 < self.width and 0 < self.height
	
	@property
	def params(self):
		return [
			self.left,
			self.top,
			self.width,
			self.height,
		]
	
	def crackx(self, other):
		"""'other' is the rectangle being cracked."""
		firstLeft = other.left
		firstRight = min(self.left, other.right)
		firstWidth = max(0, firstRight - firstLeft)
		
		secondLeft = max(self.right, other.left)
		secondRight = other.right
		secondWidth = max(0, secondRight - secondLeft)
		
		return [
			Rect(firstLeft, other.top, firstWidth, other.height),
			Rect(secondLeft, other.top, secondWidth, other.height),
		]
	
	def cracky(self, other):
		"""'other' is the rectangle being cracked."""
		firstTop = other.top
		firstBottom = min(self.top, other.bottom)
		firstHeight = max(0, firstBottom - firstTop)
		
		secondTop = max(self.bottom, other.top)
		secondBottom = other.bottom
		secondHeight = max(0, secondBottom - secondTop)
		
		return [
			Rect(other.left, firstTop, other.width, firstHeight),
			Rect(other.left, secondTop, other.width, secondHeight),
		]
	
	def crack(self, other):
		"""'other' is the rectangle being cracked."""
		verticals = self.crackx(other)
		horizontals = self.cracky(other)
		
		horizontals = [
			verticals[0].crackx(
				horizontals[0],
			)[1],
			verticals[0].crackx(
				horizontals[1],
			)[1],
		]
		
		horizontals = [
			verticals[1].crackx(
				horizontals[0],
			)[0],
			verticals[1].crackx(
				horizontals[1],
			)[0],
		]
		
		return verticals + horizontals
	
	def cleanCrack(self, other):
		return list(filter(
			lambda shard: shard.isValid(),
			self.crack(other),
		))

class LevelLoadException(Exception):
	def __init__(self, filename, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.filename = filename

def incrementable(d):
	d.counter = itertools.count()
	
	def append(value):
		index = next(d.counter)
		d[index] = value
		return index
	
	d.append = append
	
	return d

### Unit Tests

import unittest

class crackxTests(unittest.TestCase):
	def setUp(self):
		self.rect1 = Rect(400, 400, 100, 100)
	
	def test_Wrapping(self):
		rect2 = pg.Rect(350, 350, 200, 100)
		
		[leftRect, rightRect] = self.rect1.crackx(rect2)
		
		self.assertEqual(leftRect.top, 350)
		self.assertEqual(leftRect.bottom, 450)
		self.assertEqual(leftRect.left, 350)
		self.assertEqual(leftRect.right, 400)
		
		self.assertEqual(rightRect.top, 350)
		self.assertEqual(rightRect.bottom, 450)
		self.assertEqual(rightRect.left, 500)
		self.assertEqual(rightRect.right, 550)
	
	def test_Left(self):
		rect2 = pg.Rect(350, 400, 100, 100)
		
		[leftRect, rightRect] = self.rect1.crackx(rect2)
		
		self.assertEqual(leftRect.top, 400)
		self.assertEqual(leftRect.bottom, 500)
		self.assertEqual(leftRect.left, 350)
		self.assertEqual(leftRect.right, 400)
	
	def test_Right(self):
		rect2 = pg.Rect(450, 450, 100, 100)
		
		[leftRect, rightRect] = self.rect1.crackx(rect2)
		
		self.assertEqual(rightRect.top, 450)
		self.assertEqual(rightRect.bottom, 550)
		self.assertEqual(rightRect.left, 500)
		self.assertEqual(rightRect.right, 550)

class crackyTests(unittest.TestCase):
	def setUp(self):
		self.rect1 = Rect(400, 400, 100, 100)
	
	def test_Wrapping(self):
		rect2 = pg.Rect(350, 350, 100, 200)
		
		[topRect, bottomRect] = self.rect1.cracky(rect2)
		
		self.assertEqual(topRect.top, 350)
		self.assertEqual(topRect.bottom, 400)
		self.assertEqual(topRect.left, 350)
		self.assertEqual(topRect.right, 450)
		
		self.assertEqual(bottomRect.top, 500)
		self.assertEqual(bottomRect.bottom, 550)
		self.assertEqual(bottomRect.left, 350)
		self.assertEqual(bottomRect.right, 450)
	
	def test_Top(self):
		rect2 = pg.Rect(400, 350, 100, 100)
		
		[topRect, bottomRect] = self.rect1.cracky(rect2)
		
		self.assertEqual(topRect.top, 350)
		self.assertEqual(topRect.bottom, 400)
		self.assertEqual(topRect.left, 400)
		self.assertEqual(topRect.right, 500)
	
	def test_Bottom(self):
		rect2 = pg.Rect(450, 450, 100, 100)
		
		[topRect, bottomRect] = self.rect1.cracky(rect2)
		
		self.assertEqual(bottomRect.top, 500)
		self.assertEqual(bottomRect.bottom, 550)
		self.assertEqual(bottomRect.left, 450)
		self.assertEqual(bottomRect.right, 550)

if __name__ == "__main__":
	unittest.main()
