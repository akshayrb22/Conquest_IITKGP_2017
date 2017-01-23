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
from ImageProcess import Frame 
from PathOptimizer import PathOptimizer
import copy


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
        #print id.get_coordinate()
        (x, y) = id
        results = [(x+1,  y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x-1, y-1), (x+1, y-1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
    @staticmethod
    def find_obstacles(obstacle_checkPoints):
        all_obstacles=[]
        obstacle_constant = 50
        for currentPoint in obstacle_checkPoints:
            for p in range(currentPoint.center.y - obstacle_constant,currentPoint.center.y+obstacle_constant):
                for q in range(currentPoint.center.x - obstacle_constant,currentPoint.center.x + obstacle_constant):
                    all_obstacles.append((p,q))
                    all_obstacles = list(set(all_obstacles))
        return allObstacles


class AStar(object):
    graph = None
    position = Point(0,0)
    @staticmethod
    def init(gridX, gridY, array_of_obst):
        AStar.graph=Grid(gridX,gridY)
        AStar.graph.obstacles=array_of_obst
    @staticmethod  
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        distance=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
        return distance

    @staticmethod
    def writeToFile(path):

        p=open("path.txt","w")
        for point in path:
            p.write(str(point[0]) + " " + str(point[1]) + "\n")


    ##start=(0,0)
    ##goal=(900,900)

    @staticmethod
    def search(start, goal,gridX, gridY, array_of_obst):
        AStar.graph=Grid(gridX,gridY)
        AStar.graph.obstacles=array_of_obst
        frontier = PriorityQueue()
        frontier.put(AStar.position.get_coordinate(), 0)
        came_from = {}
        cost_so_far = {}
        came_from[AStar.position.get_coordinate()] = None
        cost_so_far[AStar.position.get_coordinate()] = 0
        while not frontier.empty():
            current = frontier.get()
            if current == (goal):
                break
            for next in AStar.graph.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + AStar.heuristic(goal,next)
                    frontier.put(next, priority)
                    came_from[next] = current
        path = AStar.FindPath(came_from,goal)
        path += copy.deepcopy(Grid.find_obstacles(AStar.graph.obstacles))
        AStar.writeToFile(path)
        return PathOptimizer.Optimize()

    @staticmethod
    def FindPath(came_from,goal):
        target=goal
        path=[]

        path.append(target)
        while target != Bot.position.get_coordinate():
            target = came_from[(target)]
            path.append(target)
        path.reverse()
        return path

    @staticmethod
    def PrintInImage(Image,gridX,gridY,path):
        img = np.zeros((gridX,gridY,3), np.uint8)
        a=np.zeros(shape=(gridX,gridY))
        for i in range(0,gridX):
            for j in range(0,gridY):
                if (i,j) in path:
                    img[i,j]=(255,255,255)
                
        cv2.imshow('output.jpg',img)


if __name__ == '__main__':
    obs = []
    obs.append(Checkpoint(0,Point(5,5),0,0,0))
    obs.append(Checkpoint(0,Point(6,5),0,0,0))
    obs.append(Checkpoint(0,Point(7,5),0,0,0))
    AStar.init(690,690,obs)
    optimizedPath =  AStar.search((649,649))
    print optimizedPath
    
    
    print optimizedPath
    cv2.waitKey(0)


