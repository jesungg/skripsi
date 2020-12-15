import numpy as np
import cv2 as cv
cap = cv.VideoCapture('sampel.mp4')
#kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
fgbg = cv.createBackgroundSubtractorMOG2()

#fgbg = cv.bgsegm.BackgroundSubtractorGMG()
#fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)
#fgbg = cv.createBackgroundSubtractorKNN(detectShadows=True)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    fgmask = fgbg.apply(frame)
    #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    median_blur= cv.medianBlur(fgmask, 21)
    gauss_blur= cv.GaussianBlur(fgmask, (5, 5), 0)
    contours, _=cv.findContours(median_blur,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)



    #list semua contour
    for contour in contours:
        (x,y,w,h)=cv.boundingRect(contour)
        if cv.contourArea(contour) < 1500:
            continue
        cv.rectangle(frame, (x,y),(x+w, y+h), (0,255,0), 2)
        cv.rectangle(median_blur, (x,y),(x+w, y+h), (0,255,0), 2)

        M = cv.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv.rectangle(frame, (cx,cy),(cx+1, cy+1), (255,0,0), 2)
        cv.rectangle(median_blur, (x,y),(x+w, y+h), (0,255,0), 2)
        cv.rectangle(gauss_blur, (x,y),(x+w, y+h), (0,0,255), 2)


        print (cx,cy)

        #print(x,y,w,h)
        #cv.putText(frame,"status: {}".format('Movement'), (10,20), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

    #list semua center

    #pilih 1 contour
    #pilih 1 center
    #pilih center terdekat
    #pindah contour

    cv.imshow('Frame', frame)
    cv.imshow('FG MASK+MF Frame', median_blur)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
cap.release()
cv.destroyAllWindows()