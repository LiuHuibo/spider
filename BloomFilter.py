#!usr/bin/python
#coding=UTF-8
class BloomFilter:
	def __init__(self):
		self.visited = set()


	def put(self,item):
		if item not in self.visited:
			return 0
		else:
			return -1

