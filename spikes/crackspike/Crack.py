#!/bin/python3

### Code

import pygame as pg

def crackx(rect1, rect2):
	"""'rect2' is the rectangle being cracked."""
	firstLeft = rect2.left
	firstRight = min(rect1.left, rect2.right)
	firstWidth = max(0, firstRight - firstLeft)
	
	secondLeft = max(rect1.right, rect2.left)
	secondRight = rect2.right
	secondWidth = max(0, secondRight - secondLeft)
	
	return [
		pg.Rect(firstLeft, rect2.top, firstWidth, rect2.height),
		pg.Rect(secondLeft, rect2.top, secondWidth, rect2.height),
	]

def cracky(rect1, rect2):
	"""'rect2' is the rectangle being cracked."""
	firstTop = rect2.top
	firstBottom = min(rect1.top, rect2.bottom)
	firstHeight = max(0, firstBottom - firstTop)
	
	secondTop = max(rect1.bottom, rect2.top)
	secondBottom = rect2.bottom
	secondHeight = max(0, secondBottom - secondTop)
	
	return [
		pg.Rect(rect2.left, firstTop, rect2.width, firstHeight),
		pg.Rect(rect2.left, secondTop, rect2.width, secondHeight),
	]

def crack(rect1, rect2):
	"""'rect2' is the rectangle being cracked."""
	verticals = crackx(rect1, rect2)
	horizontals = cracky(rect1, rect2)
	
	horizontals = [
		crackx(
			verticals[0],
			horizontals[0],
		)[1],
		crackx(
			verticals[0],
			horizontals[1],
		)[1],
	]
	
	horizontals = [
		crackx(
			verticals[1],
			horizontals[0],
		)[0],
		crackx(
			verticals[1],
			horizontals[1],
		)[0],
	]
	
	return verticals + horizontals

getTangible = lambda rects: list(filter(lambda rect: 0 < rect.width and 0 < rect.height, rects))

### Unit Tests

import unittest

class crackxTests(unittest.TestCase):
	def setUp(self):
		self.rect1 = pg.Rect(400, 400, 100, 100)
	
	def test_Wrapping(self):
		rect2 = pg.Rect(350, 350, 200, 100)
		
		[leftRect, rightRect] = crackx(self.rect1, rect2)
		
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
		
		[leftRect, rightRect] = crackx(self.rect1, rect2)
		
		self.assertEqual(leftRect.top, 400)
		self.assertEqual(leftRect.bottom, 500)
		self.assertEqual(leftRect.left, 350)
		self.assertEqual(leftRect.right, 400)
	
	def test_Right(self):
		rect2 = pg.Rect(450, 450, 100, 100)
		
		[leftRect, rightRect] = crackx(self.rect1, rect2)
		
		self.assertEqual(rightRect.top, 450)
		self.assertEqual(rightRect.bottom, 550)
		self.assertEqual(rightRect.left, 500)
		self.assertEqual(rightRect.right, 550)

class crackyTests(unittest.TestCase):
	def setUp(self):
		self.rect1 = pg.Rect(400, 400, 100, 100)
	
	def test_Wrapping(self):
		rect2 = pg.Rect(350, 350, 100, 200)
		
		[topRect, bottomRect] = cracky(self.rect1, rect2)
		
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
		
		[topRect, bottomRect] = cracky(self.rect1, rect2)
		
		self.assertEqual(topRect.top, 350)
		self.assertEqual(topRect.bottom, 400)
		self.assertEqual(topRect.left, 400)
		self.assertEqual(topRect.right, 500)
	
	def test_Bottom(self):
		rect2 = pg.Rect(450, 450, 100, 100)
		
		[topRect, bottomRect] = cracky(self.rect1, rect2)
		
		self.assertEqual(bottomRect.top, 500)
		self.assertEqual(bottomRect.bottom, 550)
		self.assertEqual(bottomRect.left, 450)
		self.assertEqual(bottomRect.right, 550)

if __name__ == "__main__":
	unittest.main()
