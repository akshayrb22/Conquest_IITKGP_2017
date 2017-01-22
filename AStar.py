##Assign to Akshay
##Functionalities required
##  return shortest path in an array of points(i.e coordinates)

import matplotlib.pyplot as plot
import heapq
import cv2
import numpy as np
import PIL
from PIL import Image
from BotController import Bot
from Point import Point



class PriorityQueue(object):
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        temp = heapq.heappop(self.elements)[1]
        #print temp
        return Point(temp.x,temp.y)

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
        #print id.get_coordinate()
        (x, y) = id.get_coordinate()
        results = [(x+1,  y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x-1, y-1), (x+1, y-1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
    @staticmethod
    def find_obstacles(obstacle_checkPoints):
        all_obstacles=[]
        obstacle_constant = 50
        for p in range(obstacle_checkPoints.position.y - obstacle_constant,obstacle_checkPoints.position.y+obstacle_constant):
            for q in range(obstacle_checkPoints.position.x - obstacle_constant,obstacle_checkPoints.position.x + obstacle_constant):
                all_obstacles.append(Point(p,q))
        return all_obstacles

class SimpleGraph(object):
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]


class AStar(object):
    graph = None
    position = Point(0,0)
    @staticmethod
    def init(gridX, gridY, array_of_obst):
        AStar.graph=Grid(gridX,gridY)
        AStar.graph.obstacles=array_of_obst
    @staticmethod  
    def heuristic(a, b):
        (x1, y1) = a.get_coordinate()
        (x2, y2) = b.get_coordinate()
        distance=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
        return distance



    ##start=(0,0)
    ##goal=(900,900)

    @staticmethod
    def search(goal):
        frontier = PriorityQueue()
        frontier.put(AStar.position, 0)
        came_from = {}
        cost_so_far = {}
        came_from[AStar.position] = None
        cost_so_far[AStar.position] = 0
        while not frontier.empty():
            current = frontier.get()
            print current.toString()
            if current == (goal):
                break
            for next in AStar.graph.neighbors(current):
                new_cost = cost_so_far[current.get_coordinate()] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + AStar.heuristic(goal, Point(next[0],next[1]))
                    frontier.put(next, priority)
                    came_from[next] = current
        return AStar.FindPath(came_from,goal)

    @staticmethod
    def FindPath(came_from,goal):
        target=goal
        path={}

        path.append(target)
        while target != Bot.position:
            target=came_from[target]
            path.append(target)
        path.reverse()
        return path

    @staticmethod
    def PrintInImage(Image):
        a=np.zeros(shape=(gridX,gridY))
        for i in range(0,gridX):
            for j in range(0,gridY):
                if (i,j) in path:
                    Image[i,j]=(255,255,255)
                
        cv2.imwrite('output.jpg',img)


if __name__ == '__main__':
    obs = []
    obs.append(Point(5,5))
    obs.append(Point(6,5))
    obs.append(Point(4,5))
    AStar.init(10,10,obs)
    print AStar.search(Point(10,10))


