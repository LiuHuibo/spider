#!usr/bin/python
#coding=UTF-8
class BloomFilter:
	def __init__(self):
		self.visited = set()


	def put(self,item):
		if item not in self.visited:
			self.visited.add(item)
			return 0
		else:
			return -1

