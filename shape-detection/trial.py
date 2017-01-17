import cv2
import PIL
from PIL import Image
import numpy as np
import matplotlib.pyplot as plot


img = cv2.imread('asia.jpg')
u=0
v=0
for i in range(0,570):
    for j in range(0,570):
        cv2.line(img,(u,0),(u,570),(255,0,0),1)
        cv2.line(img,(0,v),(600,v),(255,0,0),1)
        u+=30
        v+=30


#a* part
frontier = PriorityQueue()
frontier.put((cX,cY), 0)
came_from = {}
cost_so_far = {}
came_from[(cX,cY)] = None
cost_so_far[(cX,cY)] = 0

for n in range(0,19):
        for n in range(0,19):
            while not frontier.empty():
                current = frontier.get()
                if current == (cX2,cY2):
                    break
                for next in graph.neighbors(current):
                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic((cX2,cY2), next)
                        frontier.put(next, priority)
                        came_from[next] = current



        
cv2.imshow('asia',img)
print (img)

cv2.waitKey(0)
cv2.destroyAllWindows()
