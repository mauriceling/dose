"""
Data Structure: Queue.
Date created: 30th January 2021
Licence: Python Software Foundation License version 2

Implemented from https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaQueueinPython.html
"""
class Queue(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
