#other lib
import argparse
import json
import os
import time
# from idlelib.window import add_windows_to_menu
from pdb import run

import cv2
import imutils
import kivy
import numpy as np
#from Cython.Compiler.Naming import self_cname
from imutils.feature.factories import is_cv2
from imutils.video import FPS, VideoStream
#from docutils.nodes import container
#from Cython.Shadow import pointer
#from Cython.Compiler.Naming import self_cname
from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
#uix lib
#uix lib
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from numpy import ndarray

store = JsonStore('storage.json')

#from pylint import message

kivy.require('1.11.1')





#other file

#dictionaries

#kv filepath
Window.size = (800, 800)
# kv = Builder.load_file("appIOTKF.kv")

#8 screen, 4 popup
#all screen -> pass (if empty as placeholder)

class welcomeScr(Screen): #1
    pass

class openFileDiag(BoxLayout): #pop1
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class selVidScr(Screen): #2
    def dismiss_popup(self):
        #print("close popup")
        self._popup.dismiss()
    def getImg(self,fileloc):
        IMG_SAVE_PATH = "widgets/IOTKF/IOTKF/res/first_frame.png"
        vidcap = cv2.VideoCapture(fileloc)
        success, image = vidcap.read()
        if success:
            store.put('image_data',capture_path=IMG_SAVE_PATH)
            cv2.imwrite(IMG_SAVE_PATH, image)  # save frame as JPEG file
    def select(self, dirpath, filepath):
        #print('path', dirpath,type(dirpath))
        #print('filename', filepath, type(filepath))
        stringnya = str(filepath)
        stringnya = stringnya[2:-2]
        acceptedformat = 'mp4'
        print('stringnya', stringnya, type(stringnya), acceptedformat)
        print(stringnya[-3:])
        store.put('video_data',video_path=stringnya)
        if stringnya[-3:] == acceptedformat:
            print("acceptedformat")
            self.getImg(fileloc=stringnya)
            pass
        else:
            print("not accepted")
            stringnya = None 
        self.dismiss_popup()
        return stringnya
    def show_file(self):
        print("show popup")
        content = openFileDiag(select=self.select, cancel=self.dismiss_popup)
        self._popup =Popup(title="Select video file", content=content, size_hint=(.9, .9))
        self._popup.open()
    

class chooseSet(Screen): #3
    def pulldata(self):
        try:
            data=newSet().openJson()
            for json_obj in data:
                print('json_obj',json_obj)
                namaset = json_obj['namaset']
                print('namaset', namaset)
            #harus string string akses dictnya
            # print(data['3']['namaset'])
            # bykbtn = 0
            # if bykbtn == data_keys:
            #     print('stop woy')
            # for key in data_keys:
            #     if bykbtn == data_keys:
            #         print('stop woy')
            #         break
            #     keynya = data[bykbtn]['namaset']
            #     #print(keynya)
            #     createBtn = Button(text=keynya,font_size=12)
            #     self.ids.containerr.add_widget(createBtn)
            #     bykbtn=bykbtn+1


            # for key in data :
            #     print (key,len(data))


            # for n in range(len(data)):
            #     if data is None:
            #         print('no data')
            #     else:
            #         print('ada data')
            #         try:
            #             print('n=',n)   
            #             print('len=',len(data))
            #             poin=str(n+1)
            #             nama = data[poin]["namaset"]
            #             print('isi=',poin,nama)
            #             self.ids.containerr.add_widget(Button(text='nama', font_size=12))
            #             print("add W")
            #             n=n+1
            #             print('incr')
            #             if n == len(data):
            #                 break
            #         except Exception as e:
            #             print(e)
            #         # if self.ids.poin.state=='down':
            #         #     print('choosen')
            #         #     pass
            #         # else:
            #         #     pass
        except Exception as e:
            print('[ERROR] chooseSet open JSON',e)

class newSet(Screen): #4
    def show_coor(self):
        capture_path = store.get('image_data')['capture_path']
        print('stringnya',capture_path)
        events = [i for i in dir(cv2) if 'EVENT' in i]
        print(events)
        refPt = []
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
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
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.imread(capture_path)
        img = imutils.resize(img, width=600)
        cv2.imshow("image", img)
        # #calling the mouse click event
        cv2.setMouseCallback("image", click_event)
        if cv2.waitKey(0) == 27:  # if key 'q' is pressed 
            cv2.destroyWindow("image")

    def writeJson(self,payload):
        with open("widgets/IOTKF/IOTKF/res/data.json", "w") as outfile: 
            json.dump({"data":payload}, outfile) 

    def openJson(self):
        f = open('widgets/IOTKF/IOTKF/res/data.json')
        data = json.load(f)['data']
        print('you did it')
        #print(data)
        return data

    def get_variables(self):
        try:
            data=self.openJson()
            setName = self.ids.setup_name.text
            nLoc = self.ids.noise_loc.text
            nCode = self.ids.noise_code.text

            a1name = self.ids.a1nem.text
            a2name = self.ids.a2nem.text
            a3name = self.ids.a3nem.text
            a4name = self.ids.a4nem.text
            a5name = self.ids.a5nem.text
            a6name = self.ids.a6nem.text
            a7name = self.ids.a7nem.text
            a8name = self.ids.a8nem.text
            a9name = self.ids.a9nem.text
            a10name = self.ids.a10nem.text

            a1x0 = self.ids.a1xnol.text
            a2x0 = self.ids.a2xnol.text
            a3x0 = self.ids.a3xnol.text
            a4x0 = self.ids.a4xnol.text
            a5x0 = self.ids.a5xnol.text
            a6x0 = self.ids.a6xnol.text
            a7x0 = self.ids.a7xnol.text
            a8x0 = self.ids.a8xnol.text
            a9x0 = self.ids.a9xnol.text
            a10x0 = self.ids.a10xnol.text
            a1y0 = self.ids.a1ynol.text
            a2y0 = self.ids.a2ynol.text
            a3y0 = self.ids.a3ynol.text
            a4y0 = self.ids.a4ynol.text
            a5y0 = self.ids.a5ynol.text
            a6y0 = self.ids.a6ynol.text
            a7y0 = self.ids.a7ynol.text
            a8y0 = self.ids.a8ynol.text
            a9y0 = self.ids.a9ynol.text
            a10y0 = self.ids.a10ynol.text

            a1x1 = self.ids.a1xsatu.text
            a2x1 = self.ids.a2xsatu.text
            a3x1 = self.ids.a3xsatu.text
            a4x1 = self.ids.a4xsatu.text
            a5x1 = self.ids.a5xsatu.text
            a6x1 = self.ids.a6xsatu.text
            a7x1 = self.ids.a7xsatu.text
            a8x1 = self.ids.a8xsatu.text
            a9x1 = self.ids.a9xsatu.text
            a10x1 = self.ids.a10xsatu.text
            a1y1 = self.ids.a1ysatu.text
            a2y1 = self.ids.a2ysatu.text
            a3y1 = self.ids.a3ysatu.text
            a4y1 = self.ids.a4ysatu.text
            a5y1 = self.ids.a5ysatu.text
            a6y1 = self.ids.a6ysatu.text
            a7y1 = self.ids.a7ysatu.text
            a8y1 = self.ids.a8ysatu.text
            a9y1 = self.ids.a9ysatu.text
            a10y1 = self.ids.a10ysatu.text

            d_act = {'a1':{'name':a1name ,'x0':a1x0 ,'y0':a1y0 ,'x1':a1x1 ,'y1':a1y1},
                    'a2':{'name':a2name ,'x0':a2x0 ,'y0':a2y0 ,'x1':a2x1 ,'y1':a2y1},
                    'a3':{'name':a3name ,'x0':a3x0 ,'y0':a3y0 ,'x1':a3x1 ,'y1':a3y1},
                    'a4':{'name':a4name ,'x0':a4x0 ,'y0':a4y0 ,'x1':a4x1 ,'y1':a4y1},
                    'a5':{'name':a5name ,'x0':a5x0 ,'y0':a5y0 ,'x1':a5x1 ,'y1':a5y1},
                    'a6':{'name':a6name ,'x0':a6x0 ,'y0':a6y0 ,'x1':a6x1 ,'y1':a6y1},
                    'a7':{'name':a7name ,'x0':a7x0 ,'y0':a7y0 ,'x1':a7x1 ,'y1':a7y1},
                    'a8':{'name':a8name ,'x0':a8x0 ,'y0':a8y0 ,'x1':a8x1 ,'y1':a8y1},
                    'a9':{'name':a9name ,'x0':a9x0 ,'y0':a9y0 ,'x1':a9x1 ,'y1':a9y1},
                    'a10':{'name':a10name ,'x0':a10x0 ,'y0':a10y0 ,'x1':a10x1 ,'y1':a10y1}}

            if data is not None:
                print('data is not none',data)
                n_data = len(data)
                in_id = n_data
                print('n_data: {}, in_id: {}'.format(n_data,in_id))
                data.append({
                    'id': in_id,
                    'namaset': setName,
                    'nloc': nLoc,
                    'ncod': nCode,
                    'acts': d_act
                })
                print(data)
                self.writeJson(data)
                print('done write',data)
            else:
                print('data is none', data)
                new_data = []
                d_setting = {
                    'id': 1,
                    'namaset': setName,
                    'nloc': nLoc,
                    'ncod': nCode,
                    'acts': d_act
                }
                new_data.append(d_setting)
                self.writeJson(new_data)
                print(data)
            print (nLoc,nCode)
        except Exception as e:
            print ('error open json',e)



class cNoise(FloatLayout): #pop2
    pass
class addAct(FloatLayout): #pop3
    pass
class loadingScr(Screen): #5
     pass
class resultScr(Screen): #6
    #object detection
    def titiktengah(self,kontur):
        M = cv2.moments(kontur)
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
        return x, y

    def lokasi_obj(self):
        fwidth = None
        fheight = None
        nframe = 30
        sframe = 0

        phase1 = True
        phase2 = False

        x_obj = []
        y_obj = []

        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,500)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        kernel = np.ones((5,5),np.uint8)
        vid_path = store.get('video_data')['video_path']
        cap = cv2.VideoCapture(vid_path)
        fps =  FPS().start()
        #frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        ret, frame = cap.read()
        try:
            out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (600,337))
        except:
            pass

        if frame is None:
                fps.stop()
        else:
            fps.update()
            try:   
                frame = imutils.resize(frame, width=600)
                (aw, ah, ac) = frame.shape
            except Exception as e:
                print('frame resize error',e)
                pass
            
            if sframe % nframe == 0 :
                bgsub = cv2.createBackgroundSubtractorMOG2()
                fgmask = bgsub.apply(frame)
                gblur = cv2.GaussianBlur(fgmask, (11,11), 0)
                erosion = cv2.erode(fgmask,kernel,iterations = 1)
                dilation = cv2.dilate(erosion,kernel,iterations = 1)
                closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
                contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    (x,y,w,h) = cv2.boundingRect(contour)
                    cont_h = y+h
                    cont_w = x+w
                    if cv2.contourArea(contour) < 750:
                        continue
                    if cont_h < 200 :
                        continue
                    hull = cv2.convexHull(contour)
                    cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)
                    cv2.rectangle(frame, (x,y),(cont_w, cont_h), (0,255,0), 2)
                    
                    contSize = len(contour) #semua piksel sebuah kontur
                    contNum = len(contours) #semua kontur dan semua pikselnya
                    if contNum > 1:
                        print('lebih dr 1')
                        for i in range(contNum):
                            try:
                                cx, cy = self.titiktengah(hull)
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
                        cx, cy = self.titiktengah(hull)
                        x_obj.append(cx)
                        y_obj.append(cy)

                sframe += 1
                fps.update()
                # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
                out.write(frame)

            #print(x_obj, y_obj)

        #filter
        #filter
    
    pass
class resultVid(FloatLayout): #pop4
    pass
class aboutScr(Screen):
    pass
class helpScr(Screen):
    pass


#super: App
class appIOTKF(App):
    def build(self):
        scrMg = ScreenManager()
        scrMg.add_widget(welcomeScr(
            name = 'welcome_scr' #scr id
        ))
        scrMg.add_widget(selVidScr(
            name = 'sel_vid_scr'
        ))
        scrMg.add_widget(chooseSet(
            name = 'choose_set'
        ))
        scrMg.add_widget(newSet(
            name = 'new_set'
        ))
        scrMg.add_widget(loadingScr(
            name = 'loading_scr'
        ))
        scrMg.add_widget(resultScr(
            name = 'result_scr'
        ))
        scrMg.add_widget(aboutScr(
            name = 'about_scr'
        ))
        scrMg.add_widget(helpScr(
            name = 'help_scr'
        ))
        return (scrMg)

if __name__ == '__main__':
    appIOTKF().run()