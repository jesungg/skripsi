import cv2 as cv
import numpy as np
import sys

##
# 1 : target birth loc
# 2 : target birth -> centroid & draw square      
# 3 : tracking start
# 
# 
# 
# ##

#//params
tbirth_x0 = 562
tbirth_y0 = 459

tbirth_x1 = 790
tbirth_y1 = 462


# Instantiate OCV kalman filter
class KalmanFilter:

    kf = cv.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], 
                                    [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0], 
                                    [0, 1, 0, 1], 
                                    [0, 0, 1, 0], 
                                    [0, 0, 0, 1]], np.float32)

    def Estimate(self, coordX, coordY):
        ''' This function estimates the position of the object'''
        measured = np.array([[np.float32(coordX)], 
                             [np.float32(coordY)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        return predicted



#Performs required image processing to get ball coordinated in the video
class ProcessImage:

    def DetectObject(self):

        vid = cv.VideoCapture('sampel.mp4')

        if(vid.isOpened() == False):
            print('Cannot open input video')
            return

        width = int(vid.get(3))
        height = int(vid.get(4))

        # Create Kalman Filter Object
        kfObj = KalmanFilter()
        predictedCoords = np.zeros((2, 1), np.float32)

        while(vid.isOpened()):
            rc, frame = vid.read()

            if(rc == True):
                [ballX, ballY] = self.DetectBall(frame)
                predictedCoords = kfObj.Estimate(ballX, ballY)
                print(ballY)

                if ballY > 458 :
                    # Draw Actual coords from segmentation
                    cv.circle(frame, (int(ballX), int(ballY)), 20, [0,0,255], 2, 8)
                    cv.line(frame,(int(ballX), int(ballY + 20)), (int(ballX + 50), int(ballY + 20)), [100,100,255], 2,8)
                    cv.putText(frame, "Actual", (int(ballX + 50), int(ballY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])

                    # Draw Kalman Filter Predicted output
                    cv.circle(frame, (predictedCoords[0], predictedCoords[1]), 20, [0,255,255], 2, 8)
                    cv.line(frame, (predictedCoords[0] + 16, predictedCoords[1] - 15), (predictedCoords[0] + 50, predictedCoords[1] - 30), [100, 10, 255], 2, 8)
                    cv.putText(frame, "Predicted", (int(predictedCoords[0] + 50), int(predictedCoords[1] - 30)), cv.FONT_HERSHEY_SIMPLEX, 0.5, [50, 200, 250])

                    if (cv.waitKey(300) & 0xFF == ord('q')):
                        break

                else :
                    pass
                
                cv.imshow('Input', frame)


                if (cv.waitKey(300) & 0xFF == ord('q')):
                    break

            else:
                break

        vid.release()
        cv.destroyAllWindows()

    # Segment the green ball in a given frame
    def DetectBall(self, frame):

        # Set threshold to filter only green color & Filter it
        #lowerBound = np.array([130,30,0], dtype = "uint8")
        #upperBound = np.array([255,255,90], dtype = "uint8")
        #greenMask = cv.inRange(frame, lowerBound, upperBound)
        fgbg = cv.createBackgroundSubtractorMOG2()
        fgmask = fgbg.apply(frame)
        
        cv.imshow('a', fgmask)

        #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
        gauss_blur = cv.GaussianBlur(fgmask, (5,5), 0)
        contours, _=cv.findContours(gauss_blur,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Dilate
        #kernel = np.ones((5, 5), np.uint8)
        #greenMaskDilated = cv.dilate(greenMask, kernel)
        cv.imshow('Thresholded', gauss_blur)

        # Find ball blob as it is the biggest green object in the frame
        [nLabels, labels, stats, centroids] = cv.connectedComponentsWithStats(gauss_blur, 8, cv.CV_32S)

        # First biggest contour is image border always, Remove it
        stats = np.delete(stats, (0), axis = 0)
        try:
            maxBlobIdx_i, maxBlobIdx_j = np.unravel_index(stats.argmax(), stats.shape)

        # This is our ball coords that needs to be tracked
            ballX = stats[maxBlobIdx_i, 0] + (stats[maxBlobIdx_i, 2]/2)
            ballY = stats[maxBlobIdx_i, 1] + (stats[maxBlobIdx_i, 3]/2)
            return [ballX, ballY]
        except:
               pass

        return [0,0]


#Main Function
def main():

    processImg = ProcessImage()
    processImg.DetectObject()


if __name__ == "__main__":
    main()
