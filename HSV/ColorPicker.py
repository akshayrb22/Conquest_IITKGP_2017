#! /usr/bin/env python2

import cv2
import numpy as np
import imutils
from pyimagesearch.shapedetector import ShapeDetector

colors = []

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame[y,x].tolist())

def main():
    capture = cv2.VideoCapture(1)

    while True:
        _, frame = capture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS_FULL)
        if colors:
            cv2.putText(hsv, str(colors[-1]), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv2.imshow('frame', hsv)
        cv2.setMouseCallback('frame', on_mouse_click, hsv)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

    # avgb = int(sum(c[0] for c in colors) / len(colors))
    # avgg = int(sum(c[0] for c in colors) / len(colors))
    # avgr = int(sum(c[0] for c in colors) / len(colors))
    # print avgb, avgg, avgr

    minb = min(c[0] for c in colors)
    ming = min(c[1] for c in colors)
    minr = min(c[2] for c in colors)
    maxb = max(c[0] for c in colors)
    maxg = max(c[1] for c in colors)
    maxr = max(c[2] for c in colors)
    #print minr, ming, minb, maxr, maxg, maxb

    lb = [minb,ming,minr]
    ub = [maxb,maxg,maxr]
    print lb, ub


    mask = cv2.inRange(hsv, np.array(lb), np.array(ub))
    ratio = frame.shape[0] / float(frame.shape[0])
    res = cv2.bitwise_and(frame,frame, mask= mask)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    b = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.threshold(b, 0, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(b,0,0)
    cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE) 
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd=ShapeDetector
    area=0
    cX=0
    cY=0
    for c in cnts:
        M = cv2.moments(c)
        if M["m00"] > 0:
            cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
            cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
            #shape = sd.detect(c)
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            area=cv2.contourArea(c)
            if area > 310:
                cv2.drawContours(frame, [c], -1, (255,0,0), 2)
                cv2.putText(frame, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                if area > max_area:
                    max_area = area
                elif area < min_area:
                    min_area=area 
    
    #print min_area

    #print max_area                         
    cv2.imshow('mask',mask)
    cv2.imshow('resized',res)
    cv2.imshow("as",frame)
    raw_input()

if __name__ == "__main__":
    main()