import cv2 as cv
import imutils
import numpy as np
import time
import argparse

from imutils.video import VideoStream
from imutils.video import FPS

fwidth = None
fheight = None
nframe = 30
sframe = 0

phase1 = True
phase2 = False

kernel = np.ones((15,15),np.uint8)

cap = cv.VideoCapture('sampel.mp4')
bgsub = cv.createBackgroundSubtractorMOG2()
fps =  FPS().start()

while True:
    ret, frame = cap.read()
    fps.update()

    if frame is None:
        fps.stop()
        break
    
    if sframe % nframe == 0 :
        fgmask = bgsub.apply(frame)
        gblur = cv.GaussianBlur(fgmask, (5,5), 0)
        erosion = cv.erode(fgmask,kernel,iterations = 1)
        dilation = cv.dilate(erosion,kernel,iterations = 1)
        closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, kernel)
        contours, _ = cv.findContours(closing, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x,y,w,h) = cv.boundingRect(contour)
            cont_h = y+h
            cont_w = x+w
            if cv.contourArea(contour) < 3000:
                continue
            if cont_h < 470 :
                continue
            hull = cv.convexHull(contour)
            cv.rectangle(frame, (x,y),(cont_w, cont_h), (0,255,0), 2)

            M = cv.moments(hull)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv.rectangle(frame, (cx,cy),(cx+1, cy+1), (255,0,0), 2)
            cv.rectangle(gblur, (x,y),(x+w, y+h), (0,0,255), 2)
            cv.rectangle(dilation, (cx,cy),(cx+1, cy+1), (255,0,0), 2)

            
    print (cx,cy)
    cv.imshow('Frame', frame)
    #cv.imshow('FG MASK+MF Frame', gblur)
    #cv.imshow('erosion', erosion)
    #cv.imshow('closing', closing)
    cv.imshow('dilation', dilation)

    sframe += 1
    fps.update()

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        fps.stop()
        break

