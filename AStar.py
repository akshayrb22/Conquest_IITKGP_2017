##Assign to Akshay
##Functionalities required
##  return shortest path in an array of points(i.e coordinates)

import matplotlib.pyplot as plot
import heapq
import cv2
import numpy as np
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

def get_grid(gridX, gridY, array_of_obst):
    graph=Grid(gridX,gridY)
    graph.obstacles=array_of_obst
    
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    distance=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
    return distance



##start=(0,0)
##goal=(900,900)


def a_star_search(graph, start, goal,img):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while not frontier.empty():
        current = frontier.get()
        if current == (goal):
            break
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current


def FindPath(path):
    target=goal
    path.append(target)
    while target != start:
        target=came_from[target]
        path.append(target)
    print path
    
def PrintInImage(Image):
    a=np.zeros(shape=(gridX,gridY))
    for i in range(0,gridX):
        for j in range(0,gridY):
            if (i,j) in path:
                Image[i,j]=(255,255,255)
            
    cv2.imwrite('output.jpg',img)