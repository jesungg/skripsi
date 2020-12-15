import cv2 as cv
import imutils
import numpy as np
import time
import argparse

from numpy import ndarray
from imutils.video import VideoStream
from imutils.video import FPS

##functions
def titiktengah(kontur):
    M = cv.moments(kontur)
    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])
    return x, y


fwidth = None
fheight = None
nframe = 30
sframe = 0

phase1 = True
phase2 = False

x_obj = []
y_obj = []

font                   = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

kernel = np.ones((15,15),np.uint8)

cap = cv.VideoCapture('sampel.mp4')
bgsub = cv.createBackgroundSubtractorMOG2()
fps =  FPS().start()
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv.VideoWriter('outpy.avi',cv.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))


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
            cv.drawContours(frame, [hull], -1, (255, 0, 0), 2)
            cv.rectangle(frame, (x,y),(cont_w, cont_h), (0,255,0), 2)
            
            contSize = len(contour) #semua piksel sebuah kontur
            contNum = len(contours) #semua kontur dan semua pikselnya

            if contNum > 1:
                print('lebih dr 1')
                for i in range(contNum):
                    try:
                        cx, cy = titiktengah(hull)
                        if cx[i] == cx[i+1]:
                            if cy[i] == cy[i+1]:
                                pass
                            pass
                    except:
                        pass
                    i = i+1
                x_obj.append(cx)
                y_obj.append(cy)
                #print(cx,cy)
                #print(x_obj,y_obj)
            else:
                print('satu')
                cx, cy = titiktengah(hull)
                x_obj.append(cx)
                y_obj.append(cy)
                #print(cx,cy)
            print(cx,cy)
            print(x_obj)
            print(y_obj)
            
            cv.rectangle(frame, (cx,cy),(cx+1, cy+1), (255,0,0), 2)
            cv.rectangle(gblur, (x,y),(x+w, y+h), (0,0,255), 2)
            cv.rectangle(dilation, (cx,cy),(cx+1, cy+1), (255,0,0), 2)            
            #kalo contour >1
            
    cv.putText(frame,'besar kontur:' + str(contSize),
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    cv.putText(frame,'byk kontur:' + str(contNum),
        (00, 185), 
        font, 
        fontScale,
        fontColor,
        lineType)
    #print (cx,cy)
    cv.imshow('Frame', frame)
    #cv.imshow('FG MASK+MF Frame', gblur)
    #cv.imshow('erosion', erosion)
    #cv.imshow('closing', closing)
    cv.imshow('dilation', dilation)

    sframe += 1
    fps.update()
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out.write(frame)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        fps.stop()
        break