from pdb import run

import cv2 as cv
import numpy as np
from imutils.video import FPS

from widgets.IOTKF.trash.try1.deffunc import video_to_img

while True:
    fileloc = "widgets/IOTKF/sampel.mp4"
    F=video_to_img(file_loc=fileloc)
    F.run()