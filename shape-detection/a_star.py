import heapq
import cv2
import numpy as np
import PIL
from PIL import Image



class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Grid:
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
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1),(x+1,y+1),(x-1,y+1),(x-1,y-1),(x+1,y-1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]

gridX = 1000
gridY = 1000
graph=Grid(gridX,gridY)
graph.obstacles = [(400,500),(500,500),(600,500)]
img = np.zeros((gridX,gridY,3), np.uint8)
def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        distance=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
        return distance

start=(0,0)
goal=(900,900)



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



path=[]
target=goal
path.append(target)
while target != start:
    target=came_from[target]
    path.append(target)
    
    

print path
a=np.zeros(shape=(gridX,gridY))
for i in range(0,gridX):
    for j in range(0,gridY):
        if (i,j) in path:
            img[i,j]=(255,255,255)
        
cv2.imwrite('image3.jpg',img)

#cv2.imshow('p.png',img)
##if cv2.waitKey(1) & 0xFF == ord('q'):
##    
##cv2.destroyAllWindows()

    



