import cv2
import imutils
from imutils.video import FPS,VideoStream

#getvideo
# self.config_id = store.get('config_data')['selected_config_id']
# config = {}
# if self.config_id is not None:
#     data_list = newSet().openJson()
#     config = data_list[self.config_id]
# else:
#     print("[ERROR!] NO CONFIG ID")

#get t_obj, kf_x, kf_y
t_object = [7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 35, 36]
kf_x = [339.0, 318.0, 311.0, 326.0, 359.0, 395.0, 416.0, 434.0, 447.0, 455.0, 498.0, 497.0, 507.0, 517.0, 529.0, 521.0, 524.0, 522.0, 506.0, 487.0, 465.0, 443.0, 426.0, 415.0, 404.0, 395.0, 393.0]
kf_y = [265.0, 246.0, 243.0, 248.0, 260.0, 261.0, 264.0, 265.0, 267.0, 269.0, 279.0, 277.0, 274.0, 274.0, 277.0, 281.0, 284.0, 285.0, 285.0, 282.0, 279.0, 276.0, 270.0, 263.0, 259.0, 259.0, 259.0]
#start opening video
fwidth = None
fheight = None
nframe = 30
sframe = 0
pointr = 0
#kf timestep
for i in range(len(t_object)):
    t_object[i]+=1

time_kf = t_object
# addtime = t_object[-1]+1
# time_kf = []
# time_kf = t_object+[addtime]

connecting_x = []
connecting_y = []
# # print(time_kf)
dupli_ = None
# # print(addtime,'-->',time_kf)
# # cap = cv2.VideoCapture(store.get('video_data')['video_path'])
cap = cv2.VideoCapture('/Users/jesung/Documents/code/skripsi2/skripsi/widgets/sampel video/Kantor/KC1.mp4')
fps =  FPS().start()

while True:
    ret, frame = cap.read()

    fps.update()
    
    try:    
        frame = imutils.resize(frame, width=600)
        (aw, ah, ac) = frame.shape
    except:
        pass
    #ini udh ok
    if frame is None:
        fps.stop()
        break


    # everysecond do
    for i in range(len(connecting_x)):
        pass
        # try:
        #     # cv2.rectangle(frame, (connecting_x[i],connecting_y[i]), (connecting_x[i]+1, connecting_y[i]+1), (255,0,255), 2)
        #     # cv2.line(frame, (connecting_x[i],connecting_y[i]), (connecting_x[i+1],connecting_y[i+1]), (255,255,255), 2)
        # except:
        #     pass  

    if sframe % nframe == 0 :
        vtime_ = int(sframe/nframe)
        
        for i in range(len(connecting_x)):
            pass
            # try:
            #     # cv2.rectangle(frame, (connecting_x[i],connecting_y[i]), (connecting_x[i]+1, connecting_y[i]+1), (0,255,255), 2)
            #     # cv2.line(frame, (connecting_x[i],connecting_y[i]), (connecting_x[i+1],connecting_y[i+1]), (255,255,255), 2)
            # except:
            #     pass  
        vtime_ = int(sframe/nframe)
        print('sec: ',vtime_)
        print('time pointer:',time_kf[pointr])
        
        if time_kf[pointr] == vtime_:
            try:
                for i in range(len(time_kf)):
                    if vtime_ == time_kf[i]:
                        print('index->',i)
                        print('kf x->',kf_x[i])
                        print('kf y->',kf_y[i])
                        connecting_x.append(kf_x[i])
                        connecting_y.append(kf_y[i])
                        pointr+=1
                        dupli_ = True
                        # i =+ 1
            except:
                pass
            if dupli_ == True:
                print('if duplicate do something here')
                for i in range(len(connecting_x)):
                    if len(connecting_x) == 1:
                        x0=int(connecting_x[i])
                        y0=int(connecting_y[i])
                        cv2.rectangle(frame, (x0,y0), (x0+1, y0+1), (0,0,255), 2)
                    if len(connecting_x)>2:
                        try:
                            x0=int(connecting_x[i])
                            y0=int(connecting_y[i])
                            x1=int(connecting_x[i+1])
                            y1=int(connecting_y[i+1])
                            # cv2.rectangle(frame, (kf_x[i],kf_y[i]), (kf_x[i]+1, kf_y[i]+1), (0,0,255), 2)
                            cv2.line(frame, pt1=(x0,y0), pt2=(x1,y1), color=(255,255,255), thickness=2)
                            # print(connecting_x,'',connecting_y)
                        except:
                            pass
                
                dupli_ = False
            print(connecting_x,connecting_y)
            # print("masuk")
            # print(kf_x[pointr])
            
            # try:
            #     # cv2.rectangle(frame, (kf_x[i],kf_y[i]), (kf_x[i]+1, kf_y[i]+1), (0,0,255), 2)
            #     # cv2.line(frame, pt1=(int(kf_x[pointr]),int(kf_y[pointr])), pt2=(int(kf_x[pointr+1]),int(kf_y[pointr+1])), color=(255,255,255), thickness=2)
            #     # print(connecting_x,'',connecting_y)            
            # except:
            #     pass

        #loopssemua dlm 1 s
    

    # try:
    #     frame = cv2.line(frame, pt1=(int(kf_x[pointr]),int(kf_y[pointr])), pt2=(int(kf_x[pointr+1]),int(kf_y[pointr+1])), color=(255,255,255), thickness=2)
    # except:
    #     pass
    
    sframe += 1
    fps.update()

    cv2.imshow('Frame', frame)
        
        
    keyboard = cv2.waitKey(30)
    if keyboard == ord('q') or keyboard == 27:
        fps.stop()
        break


