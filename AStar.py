##Assign to Akshay
##Functionalities required
##  return shortest path in an array of points(i.e coordinates)

import matplotlib.pyplot as plot
import heapq
import cv2
import numpy as np
import PIL
from PIL import Image
from Point import Point
from ImageProcess import Frame 
from PathOptimizer import PathOptimizer
import copy
from Checkpoint import Checkpoint
from time import sleep
from Draw import Draw


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
    
        totalObstaclePoints = 0
        obstacle_range = 50
        Frame.obsBoxList = []
        for currentPoint in obstacle_checkPoints: #takes Checkpoint as input
            corner_points = [(currentPoint.center.x - obstacle_range, currentPoint.center.y - obstacle_range),
                (currentPoint.center.x + obstacle_range, currentPoint.center.y - obstacle_range),
                (currentPoint.center.x - obstacle_range, currentPoint.center.y + obstacle_range),
                (currentPoint.center.x + obstacle_range, currentPoint.center.y + obstacle_range)
            ]

            Frame.obsBoxList.append(corner_points)
            for p in range(corner_points[0][0], corner_points[1][0]): #take X coordinate
                    q = corner_points[0][1] #Y is constant
                    all_obstacles.append((p,q))
                    totalObstaclePoints += 1
                    #Frame.resized[p,q]=(255,255,255)
            for p in range(corner_points[2][0], corner_points[3][0]): #take X coordinate
                    q = corner_points[2][1]#Y is constant
                    all_obstacles.append((p,q))
                    totalObstaclePoints += 1
                    #Frame.resized[p,q]=(255,255,255)
            for p in range(corner_points[0][1], corner_points[2][1]): #take X coordinate
                    q = corner_points[0][0]  #X is contant
                    all_obstacles.append((q,p))
                    totalObstaclePoints += 1
                    #Frame.resized[q,p]=(255,255,255)
            for p in range(corner_points[1][1], corner_points[3][1]): #take X coordinate
                    q = corner_points[1][0] #X is contant
                    all_obstacles.append((q,p))
                    totalObstaclePoints += 1
                    #Frame.resized[q,p]=(255,255,255)

            lenWithDuplicates = len(all_obstacles)
            #all_obstacles = list(set(all_obstacles))
            lenWithoutDuplicates = len(all_obstacles)
        return all_obstacles
'''
        obstacle_constant = 100
        totalObstaclePoints = 0
        for currentPoint in obstacle_checkPoints:
            for p in range(currentPoint.center.y - obstacle_constant, currentPoint.center.y + obstacle_constant):
                for q in range(currentPoint.center.x - obstacle_constant, currentPoint.center.x + obstacle_constant):
                    all_obstacles.append((p,q))
                    totalObstaclePoints += 1
                    all_obstacles = list(set(all_obstacles)) '''
        


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
        AStar.graph.obstacles = Grid.find_obstacles(array_of_obst)
        AStar.position = start

        frontier = PriorityQueue()
        frontier.put(AStar.position, 0)
        came_from = {}
        cost_so_far = {}
        came_from[AStar.position] = None
        cost_so_far[AStar.position] = 0


        counter = 0
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
                    
                    print priority
            sleep(0.001)
            cv2.circle(Frame.resized,next,5,(0,0,255),2,4)
            if Frame.obsBoxList != None:
                for boundingBox in Frame.obsBoxList:
                    Draw.line(boundingBox)
            Frame.show_frame()
            counter += 1
            #if counter > 10000:
                #return None
        path = AStar.FindPath(came_from,goal)
        AStar.writeToFile(path)
        optimizedPathArray = (PathOptimizer.Optimize())
        optimizedPathList = []
        for node in optimizedPathArray:
            optimizedPathList.append((int(node[0]),int(node[1])))
        print "Optimized Path is "
        print optimizedPathList
        return optimizedPathList

    @staticmethod
    def FindPath(came_from,goal):
        target = goal
        path=[]
        print came_from
        path.append(target)
        while target != AStar.position:
            print came_from[target]
            if came_from[target] != None:
                target = came_from[target]
                path.append(target)
        path.reverse()
        return path

    @staticmethod
    def PrintInImage(gridX,gridY,path):
        img = np.zeros((gridX,gridY,3), np.uint8)
        a=np.zeros(shape=(gridX,gridY))
        for i in range(0,gridX):
            for j in range(0,gridY):
                if (i,j) in path:
                    img[i,j]=(255,255,255)
                
        cv2.imshow('output.jpg',img)


if __name__ == '__main__':
    obs = []
    obs.append(Checkpoint(0,Point(4,5),0,0,0))
    obs.append(Checkpoint(0,Point(5,5),0,0,0))
    obs.append(Checkpoint(0,Point(6,5),0,0,0))
    obs.append(Checkpoint(0,Point(7,5),0,0,0))
    AStar.init(690,690,obs)
    optimizedPath =  AStar.search((0,0),(9,9),10,10,obs)
    print optimizedPath
    AStar.PrintInImage(10,10,optimizedPath)
    raw_input()
    
    


