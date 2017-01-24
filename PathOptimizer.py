
import matplotlib.pyplot as plt
import numpy as np
import os
import rdp
class PathOptimizer:
    @staticmethod
    def Optimize():
        tolerance = 1.3 # Decrease tolerance to get a more defined path with more points  
        min_angle = np.pi*1
        filename = os.path.expanduser('path.txt')# Opening file
        points = np.genfromtxt(filename)# Reading file
        # print(points) 
        # print(len(points))
        x, y = points.T # Plotting the data

    
        simplified = np.array(rdp.rdp(points.tolist(), tolerance))
        # print(simplified)
        # print(len(simplified))
        sx, sy = simplified.T
        return(simplified)
   
if __name__ == '__main__':
    print PathOptimizer.intersecting_points()
