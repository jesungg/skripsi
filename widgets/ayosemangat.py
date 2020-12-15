import cv2 as cv
import imutils
import numpy as np
import time
import argparse
import random as rng


from numpy import ndarray
from imutils.video import VideoStream
from imutils.video import FPS

##functions
def titiktengah(kontur):
    M = cv.moments(kontur)
    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])
    return x, y

def union(a,b):
  x = min(a[0], b[0])
  y = min(a[1], b[1])
  w = max(a[0]+a[2], b[0]+b[2]) - x
  h = max(a[1]+a[3], b[1]+b[3]) - y
  return (x, y, w, h)


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

kernel = np.ones((5,5),np.uint8)

cap = cv.VideoCapture('sampel.mp4')
bgsub = cv.createBackgroundSubtractorMOG2()
fps =  FPS().start()
#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))
#try:
    #out = cv.VideoWriter('outpy.avi',cv.VideoWriter_fourcc('M','J','P','G'), 20, (600,337))
#except:
    #pass


while True:
    ret, frame = cap.read()
    fps.update()
 
        #syntax: cv2.resize(img, (width, height))
        #frame = cv.resize(frame,(aw, 600))
    try:    
        frame = imutils.resize(frame, width=600)
        (aw, ah, ac) = frame.shape
    except:
        pass

    

    if frame is None:
        fps.stop()
        break

    #every second do
    if sframe % nframe == 0 :

        #proses preprocessing 
        fgmask = bgsub.apply(frame)
        gblur = cv.GaussianBlur(fgmask, (11,11), 0)
        erosion = cv.erode(fgmask,kernel,iterations = 1)
        dilation = cv.dilate(erosion,kernel,iterations = 1)
        closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, kernel)
        
        rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 30))
        threshed = cv.morphologyEx(closing, cv.MORPH_CLOSE, rect_kernel)
        cv.imshow('threshed', threshed)


        #cari kontur
        contours, _ = cv.findContours(threshed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        #contSize = len(contour) #semua piksel sebuah kontur
        contNum = len(contours) #semua kontur dan semua pikselnya
        hull_list = []
        for i in range(len(contours)):
            (x,y,w,h) = cv.boundingRect(contours[i]) #kotakin, balikin nilai koornya
            #in piksel
            cont_h = y+h
            cont_w = x+w
            if cv.contourArea(contours[i]) < 750:
                continue
            #batas tinggi kontur >250
            if cont_h < 250 :
                continue
            hull = cv.convexHull(contours[i])
            hull_list.append(hull)
        # Draw contours + hull results
        drawing = np.zeros((closing.shape[0], closing.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            try:
                color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
                #cv.drawContours(drawing, contours, i, color)
                cv.drawContours(drawing, hull_list, i, color)
            except:
                pass

        #for every contour in contours
        for contour in contours:
            hull = cv.convexHull(contour) #point set
            (x,y,w,h) = cv.boundingRect(contour) #kotakin, balikin nilai koornya
            #in piksel
            cont_h = y+h
            cont_w = x+w
            
            #batas area kontur >750
            if cv.contourArea(contour) < 850:
                continue
            #batas tinggi kontur >200
            if cont_h < 200 :
                continue
            
            #cv.drawContours(frame, [hull], -1, (255, 0, 0), 2) #garis hull
            #cv.rectangle(frame, (x,y),(cont_w, cont_h), (0,255,0), 2) #bbox
            
            #hullNum = len(hull)
            #print ('hull' + str(hullNum))
            

            if contNum > 1:
                print('lebih dr 1')
                print(x,y,cont_h,cont_w)

                for i in range(contNum):
                    try:
                        cx, cy = titiktengah(hull)
                        #kalomisalnya duplicate skip
                        if cx[i] == cx[i+1]:
                            if cy[i] == cy[i+1]:
                                pass
                            pass
                    except:
                        pass
                    try:
                        cv.rectangle(drawing, (cx,cy), (cx+1, cy+1), (0,0,255), 2) #titik

                    except :
                        pass
                    i = i+1
                print('dlm for')
                print(x,y,cont_h,cont_w)
                #cv.rectangle(frame, (cx,cy),(cx+1, cy+1), (0,255,0), 2) #bbox
                #cv.rectangle(frame, (x,y),(cont_w, cont_h), (0,255,0), 2) #bbox
                x_obj.append(cx)
                y_obj.append(cy)
                print (x_obj)
                
                


                #print(cx,cy)
                #print(x_obj,y_obj)
            else:
                print('satu')
                cx, cy = titiktengah(hull)
                x_obj.append(cx)
                y_obj.append(cy)
                #cv.rectangle(frame, (cx,cy),(cx+1, cy+1), (0,255,0), 2) #bbox
                #cv.rectangle(frame, (x,y),(cont_w, cont_h), (0,255,0), 2) #bbox
                #print(cx,cy)
            #print(cx,cy)
            #print(x_obj)
            #print(y_obj)
            
            #cv.rectangle(gblur, (x,y),(x+w, y+h), (0,0,255), 2)
            #cv.rectangle(dilation, (cx,cy),(cx+1, cy+1), (255,0,0), 2)            
            #kalo contour >1
        try:
            for i in range (len(x_obj)):
                cv.line(frame, (x_obj[i],y_obj[i]), (x_obj[i+1],y_obj[i+1]), (0,0,255), 2) 
        except:
            pass 

    #cv.putText(frame,'besar kontur:' + str(contSize),
    #    bottomLeftCornerOfText, 
    #    font, 
    #    fontScale,
    #    fontColor,
    #    lineType)

    #cv.putText(frame,'byk kontur:' + str(contNum),
    #    (00, 185), 
    #    font, 
    #    fontScale,
    #    fontColor,
    #    lineType)
    #print (cx,cy)
    cv.imshow('Frame', frame)
    cv.imshow('Frame', drawing)

    #cv.imshow('FG MASK+MF Frame', gblur)
    #cv.imshow('erosion', erosion)
    #cv.imshow('closing', closing)
    #cv.imshow('dilation', dilation)
    #print(aw, ah)
    sframe += 1
    fps.update()
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    #out.write(frame)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        fps.stop()
        break