import numpy as np
import cv2
import imutils
import pygame
import time
import random
import math
#functions for movement in different quadrents takes in current x and y position and returns the new x,y position at the angle
#speed is number of steps to be moved in that angle
#

def first_quadCal(old_x,old_y,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    new_y = old_y - (speed*math.sin(angle_in_radians))
    return new_x, new_y

def second_quadCal(old_x,old_y,speed,angle_in_radians):
    new_x = old_x - (speed*math.cos(angle_in_radians))
    new_y = old_y - (speed*math.sin(angle_in_radians))
    return new_x, new_y
def third_quadCal(old_x,old_y,speed,angle_in_radians):
    new_x = old_x - (speed*math.cos(angle_in_radians))
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_x, new_y
def fourth_quadCal(old_x,old_y,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_x, new_y

class botMove:
    
    def __init__(self):
        self.old_x=0
        self.old_y = 0
        self.speed = 0
        self.angle_in_radians = 0
        self.x = 100
        self.y = 100
        self.display_width = 619
        self.display_height = 624
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Bot Test')

        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('a.png')
        self.marker = pygame.image.load('mark.png')
        self.angle  = 2
        pygame.init()

    def getDisplay(self):
        pygame.display.update()
        self.rect = self.marker.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.rotozoom(self.marker, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.gameDisplay.blit(self.background,(0,0))
        self.gameDisplay.blit(self.image, self.rect)

        pygame.display.flip()

        self.image1 = pygame.surfarray.array3d(self.gameDisplay)
        (h, w) = self.image1.shape[:2]
        self.center = (w // 2, h // 2)
        self.M = cv2.getRotationMatrix2D(self.center, 90, 1.0) 
        self.rotated = cv2.warpAffine(self.image1, self.M, (w, h))

        self.rgb = cv2.cvtColor(cv2.flip(self.rotated,0), cv2.COLOR_BGR2RGB)

        return self.rgb
        
    def move(self,movement):
        
        if movement == 'f':
            if(self.angle == 0 or self.angle == 360):
                self.x += 5
            if(self.angle == 90):
               self.y -= 5
            if(self.angle == 180):
                self.x -= 5
            if(self.angle == 270):
                self.y += 5
            if (0<self.angle<90):
                self.x,self.y = first_quadCal(self.x,self.y,5,math.radians(self.angle))
            if (90<self.angle<180):
                self.x,self.y = second_quadCal(self.x,self.y,5,math.radians(180-self.angle))
            if (180<self.angle<270):
                self.x,self.y = third_quadCal(self.x,self.y,5,math.radians(self.angle-180))
            if (270<self.angle<360):
                self.x,self.y = fourth_quadCal(self.x,self.y,5,math.radians(360-self.angle))
                
        if movement == 'l':
                self.angle += 2
                if(self.angle == 360):
                    self.angle = 0

                
        if movement == 'r':
                self.angle -= 2
                if(self.angle == 0):
                    self.angle = 360
      



if __name__ == '__main__':
    bot  = botMove()
    while(1):
        display = bot.getDisplay()
        bot.move('r')
        bot.move('f')
        cv2.imshow("frame",display)

        i = cv2.waitKey(5) & 0xFF
        if i == 32:
            pygame.quit()
            break
    cv2.destroyAllWindows() 
