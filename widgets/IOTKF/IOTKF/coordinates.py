import cv2
import numpy as np
import os
import imutils


#This will display all the available mouse click events  
events = [i for i in dir(cv2) if 'EVENT' in i]
# print(events)

#This variable we use to store the pixel location
refPt = []

#click event function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print()
        print(x,",",y)
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.putText(img, strXY, (x,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("image", img)

    if event == cv2.EVENT_RBUTTONDOWN:
        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        strBGR = str(blue)+", "+str(green)+","+str(red)
        cv2.putText(img, strBGR, (x,y), font, 0.5, (0,255,255), 2)
        cv2.imshow("image", img)


#Here, you need to change the image name and it's path according to your directory
img = cv2.imread(
    '/Users/jesung/Documents/code/skripsi2/skripsi/RCR5-frames/image26.jpg'
)
img = imutils.resize(img, width=600)
cv2.imshow("image", img)

# #calling the mouse click event
cv2.setMouseCallback("image", click_event)

if cv2.waitKey(0) == 27:  # if key 'q' is pressed 
    cv2.destroyWindow("image")
    



