import cv2
vidcap = cv2.VideoCapture(
    '/Users/jesung/Documents/code/skripsi2/skripsi/widgets/sampel video/Rumah/RCR5.mp4'
    )
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("image"+str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames
sec = 0
frameRate = 1 #//it will capture image in each 0.5 second
count=0 #//cb ganti 0 soalnya kalo 1 kelebihan
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)