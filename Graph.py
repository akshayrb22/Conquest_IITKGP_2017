import heapq
import numpy as np
import cv2
import matplotlib.pyplot as plot
import PIL
from PIL import Image


class PriorityQueue(object):
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):
        return id not in self.obstacles
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1,  y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x-1, y-1), (x+1, y-1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
class SimpleGraph(object):
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        distance=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
        return distance

