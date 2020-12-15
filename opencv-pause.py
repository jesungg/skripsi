import numpy as np
import cv2 as cv

cap = cv.VideoCapture('widgets/sampel.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv.imshow('frame',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    if cv.EVENT_LBUTTONDOWN :
        cv.imwrite('sampeltest.png',frame)
cap.release()
cv.destroyAllWindows()