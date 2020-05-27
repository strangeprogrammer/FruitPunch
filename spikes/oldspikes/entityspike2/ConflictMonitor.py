#!/bin/python3

### Code

class ConflictMonitor():
	def __init__(self, conflicts = {}):
		self.conflicts = conflicts
	
	def addConflicts(self, name, newConflicts): # Hashable, Set
		if name in self.conflicts:
			self.conflicts[name].update(newConflicts)
		else:
			self.conflicts[name] = newConflicts
	
	def delConflicts(self, name, newConflicts): # Hashable, Set
		if name in self.conflicts:
			self.conflicts[name].difference_update(newConflicts)
		if len(self.conflicts[name]) == 0:
			del self.conflicts[name]
	
	def hasConflict(self, name1, name2): # Hashable, String
		if name1 in self.conflicts:
			if name2 in self.conflicts[name1]:
				return True
		return False

# TODO: Add 'ReflexiveConflictMonitor'

class SymmetricConflictMonitor(ConflictMonitor):
	def addConflicts(self, name, conflicts):
		super().addConflicts(name, conflicts)
		for n in conflicts:
			super().addConflicts(n, {name})
	
	def delConflicts(self, name, conflicts):
		super().delConflicts(name, conflicts)
		for n in conflicts:
			super().delConflicts(n, {name})

class HyperConflictMonitor(ConflictMonitor):
	def addConflicts(self, newConflicts): # Set
		for name in newConflicts:
			super().addConflicts(name, newConflicts - {name})
	
	def delConflicts(self, newConflicts): # Set
		for name in newConflicts:
			super().delConflicts(name, newConflicts - {name})

### Unit Tests

import unittest
from unittest.mock import patch

class ConflictMonitorTests(unittest.TestCase):
	def throughCriteria(self, criteria, hook):
		for args, expected in criteria:
			with self.subTest(args = args, expected = expected):
				self.assertEqual(expected, hook(*args))
	
	def test_uninitialized(self):
		subject = ConflictMonitor()
		
		criteria = (
			(["name1", "name2"], False),
		)
		
		self.throughCriteria(criteria, subject.hasConflict)
	
	def test_initialized(self):
		subject = ConflictMonitor(conflicts = {0: {1}, 1: {2}, 2: {0}})
		
		self.assertEqual(subject.conflicts, {0: {1}, 1: {2}, 2: {0}})
	
	def test_add(self):
		subject = ConflictMonitor()
		subject.addConflicts(0, {1, 2, 3})
		subject.addConflicts(4, {5, 6, 7})
		
		self.assertEqual(subject.conflicts, {0: {1, 2, 3}, 4: {5, 6, 7}})
	
	def test_del1(self):
		subject = ConflictMonitor()
		subject.conflicts = {0: {1, 2, 3}, 4: {5, 6, 7}}
		subject.delConflicts(4, {5, 7})
		
		self.assertEqual(subject.conflicts, {0: {1, 2, 3}, 4: {6}})
	
	def test_del2(self):
		subject = ConflictMonitor()
		subject.conflicts = {0: {1, 2, 3}, 4: {5, 6, 7}}
		subject.delConflicts(0, {1, 2, 3})
		
		self.assertEqual(subject.conflicts, {4: {5, 6, 7}})
	
	def test_conflicts1(self):
		subject = ConflictMonitor(conflicts = {0: {1}, 1: {2}, 2: {0}})
		
		criteria1 = [
			([0, 1], True),
			([1, 0], False),
			([0, 2], False),
			([2, 0], True),
		]
		
		self.throughCriteria(criteria1, subject.hasConflict)
	
	def test_conflicts2(self):
		subject = ConflictMonitor()
		subject.addConflicts(0, {1, 2, 3})
		subject.addConflicts(4, {1, 2, 3})
		
		criteria2 = [
			([0, 2], True),
			([0, 3], True),
			([4, 2], True),
			([0, 4], False),
			([1, 2], False),
		]
		
		self.throughCriteria(criteria2, subject.hasConflict)

# TODO Write unit tests for 'SymmetricConflictMonitor'
# TODO Write unit tests for 'HyperConflictMonitor'

if __name__ == "__main__":
	unittest.main()
