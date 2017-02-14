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
from Config import Config
from Utils import Utils


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
        '''
        
        '''
        all_obstacles=[]
    
        totalObstaclePoints = 0
        obstacle_range = Config.obstacleRange #round(5 * Config.mapRatio)
        
        for currentPoint in obstacle_checkPoints: #takes Checkpoint as input

            point1 = (currentPoint.gridCenter.x - obstacle_range, currentPoint.gridCenter.y - obstacle_range)
            point2 = (currentPoint.gridCenter.x + obstacle_range, currentPoint.gridCenter.y - obstacle_range)
            point3 = (currentPoint.gridCenter.x - obstacle_range, currentPoint.gridCenter.y + obstacle_range)
            point4 = (currentPoint.gridCenter.x + obstacle_range, currentPoint.gridCenter.y + obstacle_range)

            Config.obstacleBoundingPointList.append((point2, point1))
            Config.obstacleBoundingPointList.append((point3, point1))
            Config.obstacleBoundingPointList.append((point3, point4))
            Config.obstacleBoundingPointList.append((point2, point4))

            corner_points = [point1, point2, point3, point4]

            for p in range(corner_points[0][0], corner_points[1][0] + 1): #take X coordinate
                    q = corner_points[0][1] #Y is constant
                    all_obstacles.append((p,q))
                    totalObstaclePoints += 1
                    
            for p in range(corner_points[2][0], corner_points[3][0] + 1): #take X coordinate
                    q = corner_points[2][1]#Y is constant
                    all_obstacles.append((p,q))
                    totalObstaclePoints += 1
                    
            for p in range(corner_points[0][1], corner_points[2][1] + 1): #take X coordinate
                    q = corner_points[0][0]  #X is contant
                    all_obstacles.append((q,p))
                    totalObstaclePoints += 1
                    
            for p in range(corner_points[1][1], corner_points[3][1] + 1): #take X coordinate
                    q = corner_points[1][0] #X is contant
                    all_obstacles.append((q,p))
                    totalObstaclePoints += 1

        return all_obstacles

class AStar(object):
    graph = None
    position = Point(0,0)
    found = False
    @staticmethod
    def init(gridX, gridY, array_of_obst):
        AStar.graph=Grid(gridX,gridY)
        AStar.graph.obstacles=array_of_obst
    @staticmethod  
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        distance = float((((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2))) ^ (1/2))
        return distance

    @staticmethod
    def writeToFile(path):
        '''
        param-path [Type-list]
        returns-None
        It takes in the path list and writes it to a file so that it can be used to 
        reverse the path and perform operations on the list of points. 
        '''
        p=open("path.txt","w")
        for point in path:
            p.write(str(point[0]) + " " + str(point[1]) + "\n")

    @staticmethod
    def search(start, goal,gridX, gridY, array_of_obst):
        '''
        param-start [Type-Point object], goal [Type-Point object],gridX [Type-float], gridY [Type-float], 
        array_of_obst [Type-list of Checkpoint objects]
        returns- it returns the final path list the bot ahs to follow
        This is a vital function in the program. It implements the A* algorithm. All the obstacles are taken in to 
        find_obstacles() where it appends all the obstacle pixel points to the obstacle list and returns it. 
        It then works on the A* implementation. For more info-http://www.redblobgames.com/pathfinding/a-star/introduction.html 
        '''
        AStar.graph=Grid(gridX,gridY)
        AStar.graph.obstacles = Grid.find_obstacles(array_of_obst)
        AStar.position = start
        AStar.found = False

        frontier = PriorityQueue()
        frontier.put(AStar.position, 0)
        came_from = {}
        cost_so_far = {}
        came_from[AStar.position] = None
        cost_so_far[AStar.position] = 0


        counter = 0
        while not frontier.empty():
            current = frontier.get()
            
            #if current == (goal):
            #    AStar.found = True
            #    break
            for next in AStar.graph.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + AStar.heuristic(goal,next)
                    frontier.put(next, priority)
                    came_from[next] = current
            cv2.circle(Frame.resized,Utils.remapPoint(Point(next[0],next[1])).get_coordinate(),5,(0,0,255),2,4)
            if Config.obstacleBoundingPointList != None:
                    Draw.boundingBox(Config.obstacleBoundingPointList)
            #show preview of Path finding
            #Frame.show_frame()
        #if AStar.found:
        path = AStar.FindPath(came_from,goal)
        # else:
        #     print "Failed to find path!!!!! Bot or Target is inside Obstacle Range!!!!  XD"
        #     sleep(10)
        #     return None
        AStar.writeToFile(path)
        optimizedPathArray = (PathOptimizer.Optimize())
        optimizedPathList = []
        for node in optimizedPathArray:
            optimizedPathList.append(Utils.remapPoint(Point(int(node[0]),int(node[1]))).get_coordinate())
        print "Optimized Path is "
        print optimizedPathList
        return optimizedPathList

    @staticmethod
    def FindPath(came_from,goal):
        '''
        param- it take's in the previous point and the goal points
        returns- the path 
        This function returns the reverse of the path so that it can go to the resource and come back in one shot.
        It basically sets the whole path as-[path to resource point, path back to starting point].
        '''
        target = goal
        path=[]
        #print came_from
        path.append(target)
        while target != AStar.position:
            #print came_from[target]
            #if came_from[target] != None:
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
    Config.FrameWidth = 10
    Config.FrameHeight = 10
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
    
    


