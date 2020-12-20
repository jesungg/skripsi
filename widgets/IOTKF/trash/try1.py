import cv2 as cv
import numpy as np
from imutils.video import FPS

class deffunc:
    def video_to_img(self, file_loc):
        try:
            nframe = 30
            sframe = 0
            cap = cv.VideoCapture(file_loc)
            _, n_frame = cap.read()
            fps = FPS.start()
            fps.update()
            if n_frame is None:
                fps.stop()
                return 0
            if sframe % nframe == 0 :
                if sframe == 1:
                    cv.imwrite("screenshot.png", n_frame ) #filename, 
                    return print("image done")
        except cv.error as e:
            print(e)
        except Exception as e:
            print(e)
