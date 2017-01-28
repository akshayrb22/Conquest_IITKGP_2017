import cv2
import numpy as np

cap=cv2.VideoCapture(1)
res, i = cap.read(1)
cv2.imwrite("cali.png",i)