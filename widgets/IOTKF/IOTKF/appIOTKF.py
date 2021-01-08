#other lib
import argparse
import json
import math
import os
import time
from fileinput import filename
from turtledemo.chaos import plot

import cv2
import filterpy
import imutils
import kivy
import matplotlib.pyplot as plt
import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from filterpy.kalman.kalman_filter import predict, update
from imutils.feature.factories import is_cv2
from imutils.video import FPS, VideoStream
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
from kivy.uix.image import Image
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
        # print('stringnya', stringnya, type(stringnya), acceptedformat)
        # print(stringnya[-3:])
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
        self._popup =Popup(title="Pilih file video", content=content, size_hint=(.9, .9))
        self._popup.open()
    

class chooseSet(Screen): #3
    config_id = None
    def on_state(self, widget, value):
        if value == 'down':
            data_list = newSet().openJson()
            curr_config = {}
            # cari config di json
            for obj in data_list:
                if obj['namaset'] == widget.text:
                    curr_config = obj
                    self.config_id = curr_config['id']
            img = Image(source=curr_config['capture_path'])
            self.ids.container_gb.clear_widgets()
            self.ids.container_gb.add_widget(img)
        if value == 'normal':
            self.ids.container_gb.clear_widgets()
        # print('self', self)
        # print('widget',widget.text)
        # print('value',value)
        # print('========')

    def handle_delete(self):
        if self.config_id is not None :
            data_list = newSet().openJson()
            data_list[self.config_id]['is_delete'] = 'true'
            newSet().writeJson(data_list)
            self.pulldata()

    def pulldata(self):
        try:
            self.ids.containerr.clear_widgets()
            self.ids.container_gb.clear_widgets()
            print("clearwidget")
            data=newSet().openJson()
            #print(data)
            for json_obj in data:
                if json_obj['is_delete'] == 'false':
                    print('json_obj',json_obj)
                    namaset = json_obj['namaset']
                    print('namaset', namaset)
                    create_btn = ToggleButton(text=namaset, group="config")
                    create_btn.bind(state=self.on_state)
                    self.ids.containerr.add_widget(create_btn)
            if len(self.ids.containerr.children) == 0:
                # handle empty config
                empty_config_label = Label(text="no config available")
                self.ids.containerr.add_widget(empty_config_label)
        except Exception as e:
            print('[ERROR] chooseSet open JSON',e)

    def handleNext(self, sm):
        if self.config_id is not None:
            store.put('config_data',selected_config_id=self.config_id)
            sm.current = 'result_scr'

class newSet(Screen): #4
    def show_coor(self):
        capture_path = store.get('image_data')['capture_path']
        #print('stringnya',capture_path)
        events = [i for i in dir(cv2) if 'EVENT' in i]
        #print(events)
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

            in_cont_H = self.ids.cont_height.text
            in_cont_L = self.ids.cont_large.text

            noiseX0 = self.ids.noise_x0.text
            noiseY0 = self.ids.noise_y0.text
            noiseX1 = self.ids.noise_x1.text
            noiseY1 = self.ids.noise_y1.text

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
                # print('data is not none',data)
                n_data = len(data)
                in_id = n_data
                #print('n_data: {}, in_id: {}'.format(n_data,in_id))
                data.append({
                    'id': in_id,
                    'namaset': setName,
                    'is_delete': 'false',
                    'video_path': store.get('video_data')['video_path'],
                    'capture_path': store.get('image_data')['capture_path'],
                    'nloc': nLoc,
                    'ncod': nCode,
                    'nx0': noiseX0,
                    'ny0': noiseY0,
                    'nx1': noiseX1,
                    'ny1': noiseY1,
                    'in_cont_h': in_cont_H,
                    'in_cont_l': in_cont_L,
                    'acts': d_act
                })
                #print(data)
                self.writeJson(data)
                print('done write',data)
            else:
                print('data is none', data)
                new_data = []
                d_setting = {
                    'id': 1,
                    'namaset': setName,
                    'is_delete': 'false',
                    'video_path': store.get('video_data')['video_path'],
                    'capture_path': store.get('image_data')['capture_path'],
                    'nloc': nLoc,
                    'ncod': nCode,
                    'nx0': noiseX0,
                    'ny0': noiseY0,
                    'nx1': noiseX1,
                    'ny1': noiseY1,
                    'in_cont_h': in_cont_h,
                    'in_cont_l': in_cont_l,
                    'acts': d_act
                }
                new_data.append(d_setting)
                self.writeJson(new_data)
                #print(data)
            print (nLoc,nCode)
        except Exception as e:
            print ('error open json',e)


#-----finally unused-------
class cNoise(FloatLayout): #pop2
    pass
class addAct(FloatLayout): #pop3
    pass
class loadingScr(Screen): #5
    pass

class SaveDialog(FloatLayout):
    save_plot = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class resultScr(Screen): #6
    config_id = None
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    # displayed_img = None
    def show_save(self):
        content = SaveDialog(save_plot=self.save_plot, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def save_plot(self, path, filename):
        IMG = cv2.imread('final_plot_img.png')
        IMGPATH = path+'/'+filename+'.png'
        cv2.imwrite(str(IMGPATH),IMG)

        self.dismiss_popup()




    def write_desc(self):
        data_file = newSet().openJson()
        config = data_file[self.config_id]
        acts = config['acts']
        get_seconds = config['output']['object_detection']
        x_to_s = get_seconds['x_obj']
        kalman_filter = config['output']['kalman_filter']
        kfx = kalman_filter['kf_x']
        kfy = kalman_filter['kf_y']
        to_evaluate = {}
        out = []
        # sekon = []
        #buat filter data aksi kosong
        for key in acts.keys():
            is_evaluated = True
            ax = acts[key]
            for value in ax.values():
                if value == '':
                    is_evaluated = False
                    break
            if is_evaluated:
                to_evaluate[key] = ax
        print('after filtered',to_evaluate)

        for key in to_evaluate.keys():
            ax = to_evaluate[key]
            x0 = int(ax['x0'])
            y0 = int(ax['y0'])
            x1 = int(ax['x1'])
            y1 = int(ax['y1'])
            isValid = False
            print()
            print('ax nya', ax)
            for i in range(len(kfx)):
                print()
                #start dr 0
                #print(i)
                cx = int(kfx[i])
                cy = int(kfy[i])
                print('cx: {}, cy: {}'.format(cx,cy))
                if x0 <= cx <= x1:
                    if y0 <= cy <= y1:
                        # print('kf ke',i+1)
                        # print('second ke',(i+1+3))
                        # print(sekon)
                        # print('aksi:',ax['name'])
                        # print("valid")
                        # sekon.append([int(i+1+3),ax['name']])
                        isValid = True
                        break
                    break

            if isValid:
                print('valid', ax['name'])
                action = ax['name']
                out.append(action)

        data_file[self.config_id]['output']['desc'] = out
        newSet().writeJson(data_file)
        # for i in range(len(sekon)):
        #     time_ = sekon[i][0]
        #     act_ = sekon[i][1]
        #     print(time_,act_)
        #     action = str(act_) + " di detik ke-"+ str(time_)
        #     label = Label(text=action)
        #     self.ids.result_box.add_widget(label)

        for i in range(len(out)):
            action = out[i]
            label = Label(text=action)
            #label = Label(text = sekon[0][1])
            self.ids.result_box.add_widget(label)

    def kf(self,x_obj,y_obj):
        #list posisi objek
        pos_x = x_obj
        pos_y = y_obj
        kf_res_x = []
        kf_res_y = []
        kf_res_vx = []
        kf_res_vy = []

        def vel(alist):
            vel_list = [0.]
            for i in range(len(alist)):
                j = i+1
                # print(i)
                # print(alist[i])
                try:
                    vel_list.append(alist[j] - alist[i])
                except:
                    pass
            return vel_list

        #list acceleration; input=vel_list
        def accel(alist):
            accel_list = [0., 0.]
            try:
                if not alist[2]:
                    pass
                else:
                    for i in range(len(alist)):
                        j = i+1
                        k = j+1
                        accel_list.append(alist[k]-alist[j]) 
            except:
                pass
            return accel_list

        #list error
        def sqrt_alist(alist): #input alist= _min_avg yang mau di kuadrat
            sqrt_list=[]
            for i in range(len(alist)):
                sqrt_list.append(round((alist[i]**2), 2))
            return sqrt_list

        def avgpos(alist):
            average = sum(alist) / len(alist)
            average = round(average, 2)
            return average

        def avgvel(alist):
            average = sum(alist) / (len(alist)-1)
            average = round(average, 2)
            return average

        def pos_min_avg(alist):
            min_avg = []
            try:
                for i in range(len(alist)):
                    min_aver = alist[i] - avgpos(alist)
                    min_avg.append(round(min_aver, 2))
            except:
                pass
            return min_avg

        def vel_min_avg(alist):
            min_avg = [0.]
            for i in range(len(alist)):
                j = i+1
                try:
                    min_avg.append(round((alist[j] - avgvel(alist)), 2))
                except:
                    pass
            return min_avg

        #standar deviasi
        def stdpos(alist): #input=list yang udh di kuadrat
            n = len(alist) 
            std = math.sqrt( (1/(n-1)) * sum(alist) )
            return std

        def stdvel(alist): #input=list yang udh di kuadrat; -2 soalnya isi mulai dr index 1
            n = len(alist)
            std = math.sqrt( (1/(n-2)) * sum(alist) )
            return std

        vel_x = vel(pos_x)
        vel_y = vel(pos_y)
        accelx = accel(pos_x)
        accely = accel(pos_y)

        var_x = stdpos( sqrt_alist( pos_min_avg(pos_x) ) )
        var_y = stdpos( sqrt_alist( pos_min_avg(pos_y) ) )
        var_vx = stdvel( sqrt_alist( vel_min_avg(vel_x) ) )
        var_vy = stdvel( sqrt_alist( vel_min_avg(vel_y) ) )


        ### TRACKING POSITION AND VELOCITY FROM POSITIONS ###

        # CONSTRUCT OBJECTS DIMENSIONALITY (4x1 dengan 4x4)
        f = KalmanFilter( dim_x = 4,
                        dim_z = 4 )

        # ASSIGN INIT VALUES (proses mengkuti contoh soal)
        f.x = np.array([ pos_x[2],
                        pos_y[2],      #position
                        vel_x[2],
                        vel_y[2] ])    #velocity

        # DEF STATE TRANSITION MATRIX
        f.F = np.array([ [1., 0., 1., 0.],
                        [0., 1., 0., 1.],
                        [0., 0., 1., 0.], 
                        [0., 0., 0., 1.] ])
        f.B = np.array([ [.5, 0.],
                        [0., .5],
                        [1., 0.], 
                        [0., 1.] ])
        f.u = np.array([ accelx[2],
                        accely[2] ])

        # DEF MEASUREMENT FUNCTION
        f.H = np.array([ [1., 0., 0., 0.],
                        [0., 1., 0., 0.],
                        [0., 0., 1., 0.], 
                        [0., 0., 0., 1.] ])

        # DEF COVARIANCE MATRIX
        f.P = np.array([ [.9*((var_x)**2), 0., 1., 0.],
                        [0., .9*((var_y)**2), 0., 1.],
                        [0., 0., .9*((var_vx)**2), 0.], 
                        [0., 0., 0., .9*((var_vy)**2)] ])

        # ASSIGN MEASUREMENT NOISE
        f.R = np.array([ [(var_x)**2, 0., 1., 0.],
                        [0., (var_y)**2, 0., 1.],
                        [0., 0., (var_vx)**2, 0.], 
                        [0., 0., 0., (var_vy)**2] ])

        # ASSIGN PROCESS NOISE  
        f.Q = np.zeros((4,4))

        #sensor input
        # def sensor_read():
        #     a =np.array([ [231.],
        #                 [77.],      #position
        #                 [ np.negative(26.)],
        #                 [4.] ])    #velocity
        #     return a

        # PREDICT UPDATE LOOP
        for i in range(len(accelx)-3): #masi kebanyakan len nya mknya out of range
            z = np.array([ pos_x[i+3],
                        pos_y[i+3],      #position
                        vel_x[i+3],
                        vel_y[i+3] ])    #velocity    
            try:
                f.u = np.array([ accelx(i+3),
                                accely(i+3)  ])
            except:
                pass
            f.predict()
            f.update(z)
            kf_res_x.append(np.round(f.x[0]))
            kf_res_y.append(np.round(f.x[1]))
            kf_res_vx.append(np.round(f.x[2]))
            kf_res_vy.append(np.round(f.x[3]))

            # print('input z:')
            # print(z)
            # print('===========KF============')
            # print("predict: ",f.x_prior)
            # print("update: ",f.x)
            # print('=========================')

            

        print('kf_x: {}'.format(kf_res_x))
        print('kf_y: {}'.format(kf_res_y))
        guess_noise=.9*((var_vy)**2)
        # print(guess_noise)
        # print(var_x,var_y,var_vx,var_vy)
        # print(f.R)
        out = {
            'f_R': f.R.tolist(),
            'kf_x': kf_res_x,
            'kf_y': kf_res_y,
            'kf_vx': kf_res_vx,
            'kf_vy': kf_res_vy,
            'guess_noise': .9
        }
        return out
    
    def show_video(self):

        self.config_id = store.get('config_data')['selected_config_id']
        config = {}
        if self.config_id is not None:
            data_list = newSet().openJson()
            config = data_list[self.config_id]
        else:
            print("[ERROR!] NO CONFIG ID")

        
        t_object = config['output']['object_detection']['t_obj']
        _x = config['output']['object_detection']['x_obj']
        _y = config['output']['object_detection']['y_obj']
        kf_x = config['output']['kalman_filter']['kf_x']
        kf_y = config['output']['kalman_filter']['kf_y']

        #start opening video
        fwidth = None
        fheight = None
        nframe = 30
        sframe = 0
        pointr = 0
        connecting_x = []
        connecting_kfx = []
        connecting_y = []
        connecting_kfy = []
        # # print(time_kf)
        dupli_ = None
        dupli_kf = None
        for i in range(len(t_object)):
            t_object[i]+=1
        time_kf = t_object


        # # print(addtime,'-->',time_kf)
        cap1 = cv2.VideoCapture(store.get('video_data')['video_path'])
        cap2 = cv2.VideoCapture(store.get('video_data')['video_path'])
        # cap = cv2.VideoCapture('/Users/jesung/Documents/code/skripsi2/skripsi/widgets/sampel video/Kantor/KC1.mp4')
        fps =  FPS().start()

        while True:
            ret, frame1 = cap1.read()
            ret, frame2 = cap2.read()

            fps.update()
            
            try:    
                frame1 = imutils.resize(frame1, width=600)
                (aw, ah, ac) = frame1.shape
                frame2 = imutils.resize(frame2, width=600)
                (aw0, ah0, ac0) = frame1.shape
            except:
                pass

            #ini udh ok
            if frame1 is None:
                fps.stop()
                break

            if frame2 is None:
                fps.stop()
                break

            try:
                for i in range(len(connecting_kfx)):
                    if len(connecting_kfx) == 1:
                        x0=int(connecting_kfx[i])
                        y0=int(connecting_kfy[i])
                        cv2.rectangle(frame2, (x0,y0), (x0+1, y0+1), (0,0,255), 2)
                    if len(connecting_kfx)>2:
                        try:
                            x0=int(connecting_kfx[i])
                            y0=int(connecting_kfy[i])
                            x1=int(connecting_kfx[i+1])
                            y1=int(connecting_kfy[i+1])
                            # cv2.rectangle(frame, (kf_x[i],kf_y[i]), (kf_x[i]+1, kf_y[i]+1), (0,0,255), 2)
                            cv2.line(frame2, pt1=(x0,y0), pt2=(x1,y1), color=(255,255,255), thickness=2)
                            # print(connecting_x,'',connecting_y)
                        except:
                            pass
                for i in range(len(connecting_x)):
                    if len(connecting_x) == 1:
                        x0=int(connecting_x[i])
                        y0=int(connecting_y[i])
                        cv2.rectangle(frame1, (x0,y0), (x0+1, y0+1), (0,0,255), 2)
                    if len(connecting_x)>2:
                        try:
                            x0=int(connecting_x[i])
                            y0=int(connecting_y[i])
                            x1=int(connecting_x[i+1])
                            y1=int(connecting_y[i+1])
                            # cv2.rectangle(frame, (kf_x[i],kf_y[i]), (kf_x[i]+1, kf_y[i]+1), (0,0,255), 2)
                            cv2.line(frame1, pt1=(x0,y0), pt2=(x1,y1), color=(255,255,255), thickness=2)
                            # print(connecting_x,'',connecting_y)
                        except:
                            pass
            except:
                pass

            if sframe % nframe == 0 :
                vtime_ = int(sframe/nframe)
                
                # print('sec: ',vtime_)
                # try:
                #     print('time pointer:',t_object[pointr])
                # except:
                #     pass
                try:
                    if t_object[pointr] == vtime_:
                        try:
                            for i in range(len(t_object)):
                                if vtime_ == t_object[i]:
                                    print('index->',i)
                                    print('x->',_x[i])
                                    print('y->',_y[i])
                                    connecting_x.append(_x[i])
                                    connecting_y.append(_y[i])
                                    pointr+=1
                                    dupli_ = True
                                    # i =+ 1
                            for i in range(len(time_kf)):
                                if vtime_ == time_kf[i]:
                                    print('index->',i)
                                    print('kf x->',kf_x[i])
                                    print('kf y->',kf_y[i])
                                    connecting_kfx.append(kf_x[i])
                                    connecting_kfy.append(kf_y[i])
                                    pointr+=1
                                    dupli_kf = True
                        except:
                            pass
                        if dupli_ == True:
                            print('if duplicate do something here')
                            for i in range(len(connecting_x)):
                                if len(connecting_x) == 1:
                                    x0=int(connecting_x[i])
                                    y0=int(connecting_y[i])
                                    cv2.rectangle(frame1, (x0,y0), (x0+1, y0+1), (0,0,255), 2)
                                if len(connecting_x)>2:
                                    try:
                                        x0=int(connecting_x[i])
                                        y0=int(connecting_y[i])
                                        x1=int(connecting_x[i+1])
                                        y1=int(connecting_y[i+1])
                                        # cv2.rectangle(frame, (kf_x[i],kf_y[i]), (kf_x[i]+1, kf_y[i]+1), (0,0,255), 2)
                                        cv2.line(frame1, pt1=(x0,y0), pt2=(x1,y1), color=(255,255,255), thickness=2)
                                        # print(connecting_x,'',connecting_y)
                                    except:
                                        pass
                            dupli_ = False
                        
                        if dupli_kf == True:
                            for i in range(len(connecting_kfx)):
                                if len(connecting_kfx) == 1:
                                    x0=int(connecting_kfx[i])
                                    y0=int(connecting_kfy[i])
                                    cv2.rectangle(frame2, (x0,y0), (x0+1, y0+1), (0,0,255), 2)
                                if len(connecting_kfx)>2:
                                    try:
                                        x0=int(connecting_kfx[i])
                                        y0=int(connecting_kfy[i])
                                        x1=int(connecting_kfx[i+1])
                                        y1=int(connecting_kfy[i+1])
                                        # cv2.rectangle(frame, (kf_x[i],kf_y[i]), (kf_x[i]+1, kf_y[i]+1), (0,0,255), 2)
                                        cv2.line(frame2, pt1=(x0,y0), pt2=(x1,y1), color=(255,255,255), thickness=2)
                                        # print(connecting_x,'',connecting_y)
                                    except:
                                        pass
                            dupli_kf = False

                        print(connecting_x,connecting_y)
                except:
                    pass
            sframe += 1
            fps.update()

            final=cv2.vconcat([frame1,frame2])
            cv2.imshow('Frame', final)
                
                
            keyboard = cv2.waitKey(30)
            if keyboard == ord('q') or keyboard == 27:
                fps.stop()
                break
        print('writing image')
        cv2.imwrite("final_image.png", final)
        print('start drawing')
        gbr_result= Image(source='final_image.png')
        print('drawing fin')

        #try plotting
        plotx_=_x+[None]
        ploty_=_y+[None]
        plot_kfx=[None,None,None,None]+kf_x
        plot_kfy=[None,None,None,None]+kf_y
        plot_t = [0]+t_object
        plot_tkf = [0]+time_kf

        plt.style.use('seaborn-whitegrid')
        plt.subplot(2,1,1)
        plt.plot(plot_t, plotx_)
        plt.plot(plot_tkf, plot_kfx)
        # plt.plot(t ,plotx_)
        plt.ylabel('x-axis')

        plt.subplot(2,1,2)
        plt.plot(plot_t, ploty_)
        plt.plot(plot_tkf, plot_kfy)
        plt.xlabel('time (s)')
        plt.ylabel('y-axis')

        plt.savefig('final_plot_img.png')
        plot_result= Image(source='final_plot_img.png')

        self.ids.img_box.add_widget(gbr_result)
        self.ids.plot_box.add_widget(plot_result)

    def save():
        pass


        



    #object detection
    def titiktengah(self, kontur):
        M = cv2.moments(kontur)
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
        return x, y

    def lokasi_obj(self):
        self.config_id = store.get('config_data')['selected_config_id']
        # print('ada gak?', self.config_id)
        config = {}
        if self.config_id is not None:
            data_list = newSet().openJson()
            config = data_list[self.config_id]
        else:
            print("[ERROR!] NO CONFIG ID")
        fwidth = None
        fheight = None
        nframe = 30
        sframe = 0

        phase1 = True
        phase2 = False

        x_obj = []
        y_obj = []
        t_obj = []

        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,500)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        kernel = np.ones((5,5),np.uint8)

        cap = cv2.VideoCapture(store.get('video_data')['video_path'])
        bgsub = cv2.createBackgroundSubtractorMOG2()
        fps =  FPS().start()
        # try:
        #     out = cv2.VideoWriter('obdet.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (600,337))
        # except:
        #     pass


        while True:
            ret, frame = cap.read()
            fps.update()
        
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
                #sframe akumulasi tiap 30frame
                #print(sframe,nframe)

                #proses preprocessing 
                fgmask = bgsub.apply(frame)
                gblur = cv2.GaussianBlur(fgmask, (11,11), 0)
                erosion = cv2.erode(fgmask,kernel,iterations = 1)
                dilation = cv2.dilate(erosion,kernel,iterations = 1)
                closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
                rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
                threshed = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, rect_kernel)

                #cari kontur
                contours, _ = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                contNum = len(contours) #semua kontur dan semua pikselnya
                hull_list = []

                for i in range(contNum):
                    (x,y,w,h) = cv2.boundingRect(contours[i]) #kotakin, balikin nilai koornya
                    #in piksel
                    cont_h = y+h
                    cont_w = x+w
                    
                    in_cont_h = config['in_cont_h']
                    in_cont_l = config['in_cont_l']

                    #default variable
                    if in_cont_h == "":
                        in_cont_h = 0
                    else:
                        in_cont_h = int(in_cont_h)
                    if in_cont_h < 0 :
                        in_cont_h = 0

                    if in_cont_l == "":
                        in_cont_l = 0
                    else:
                        in_cont_l = int(in_cont_l)

                    if in_cont_l < 0 :
                        in_cont_l = 0
                    

                    #overall byk piksel kurang dari ini skip (h: 750,600 (kantor))(rumah 400&20)
                    if cv2.contourArea(contours[i]) < in_cont_l:
                        continue
                    #tinggi kurang dr ini skip
                    if cont_h < in_cont_h :
                        continue

                    #hull
                    hull = cv2.convexHull(contours[i])
                    hull_list.append(hull)
                    drawing = np.zeros((closing.shape[0], closing.shape[1], 3), dtype=np.uint8)
                    #ambil centroid & ilangin duplikat
                    cx, cy = self.titiktengah(hull)
                    noise_cd = config['ncod'].upper()
                    noise_lc = config['nloc']
                    noise_x0 = config['nx0']
                    noise_y0 = config['ny0']
                    noise_x1 = config['nx1']
                    noise_y1 = config['ny1']

                    # set default noise loc,x,y
                    if noise_lc == "":
                        noise_lc = 0
                    else:
                        noise_lc = int(noise_lc)
                    if noise_lc < 0 :
                        noise_lc = 0
                    
                    if noise_x0 == "":
                        noise_x0 = 0
                    else:
                        noise_x0 = int(noise_x0)
                    if noise_x0 < 0 :
                        noise_x0 = 0

                    if noise_x1 == "":
                        noise_x1 = 0
                    else:
                        noise_x1 = int(noise_x1)
                    if noise_x1 < 0 :
                        noise_x1 = 0

                    if noise_y0 == "":
                        noise_y0 = 0
                    else:
                        noise_y0 = int(noise_y0)
                    if noise_y0 < 0 :
                        noise_y0 = 0

                    if noise_y1 == "":
                        noise_y1 = 0
                    else:
                        noise_y1 = int(noise_y1)
                    if noise_y1 < 0 :
                        noise_y1 = 0
                    
                    if noise_cd =='HT':
                        if cy < noise_lc:
                            continue
                    if noise_cd =='HB':
                        if cy > noise_lc:
                            continue
                    if noise_cd =='VL':
                        if cx < noise_lc:
                            continue
                    if noise_cd =='VR':
                        if cx > noise_lc:
                            continue
                    # print('titik:', cx, cy)
                    # print(noise_x0,noise_x1,' ',noise_y0,noise_y1)

                    # if cx>noise_x0:
                    #     if cx<noise_x1:
                    #         print(noise_x0,'<',cx,'<',noise_x1)
                    #         if cy>noise_y0:
                    #             if cy<noise_y1:
                    #                 print(noise_y0,'<',cy,'<',noise_y1)
                    #                 print('filtered')
                    #                 continue
                    
                    if noise_x0 < cx < noise_x1:
                        # print(noise_x0,'<',cx,'<',noise_x1)
                        if noise_y0 < cy < noise_y1:
                            # print(noise_y0,'<',cy,'<',noise_y1)
                            # print('filtered')
                            continue
                    

                    if contNum > 1:
                        try:
                            if cx[i] == cx[i+1]:
                                if cy[i] == cy[i+1]:
                                    pass
                        except:
                            pass
                        # cv2.rectangle(frame, (cx,cy), (cx+1, cy+1), (0,0,255), 2) #titik
                        # print('frame rates :', float(sframe/30))
                        # print('locations :', cx,cy)
                        time_=int(sframe/30)
                        x_obj.append(cx)
                        y_obj.append(cy)
                        t_obj.append(time_)
                    else:
                        # cv2.rectangle(frame, (cx,cy), (cx+1, cy+1), (0,0,255), 2) #titik
                        # print('frame rates :', sframe)
                        time_=int(sframe/30)
                        x_obj.append(cx)
                        y_obj.append(cy)
                        if not x_obj:
                            pass
                        else:
                            t_obj.append(time_)

        #mustinya sih ini buat gambarnya doang ya
            # Draw contours + hull results
                # for i in range(len(contours)):
                #     try:
                #         color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
                #         cv2.drawContours(drawing, hull_list, i, color)
                #     except:
                #         pass
                # try:
                #     for i in range (len(x_obj)): 
                #         #tadinya drawing
                #         cv2.line(frame, (x_obj[i],y_obj[i]), (x_obj[i+1],y_obj[i+1]), (255,255,255), 2) 
                # except:
                #     pass

            # =======jgn lupa dibuka=======
            #  =====blocked only for testing========
            # cv2.imshow('Frame', frame)
            #self.ids.result_img.source = drawing
            sframe += 1
            
            fps.update()
            # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
            # out.write(drawing)

            keyboard = cv2.waitKey(30)
            if keyboard == ord('q') or keyboard == 27:
                fps.stop()
                break
        print('saving x and y obj')
        print('x_obj: {}'.format(x_obj))
        print('y_obj: {}'.format(y_obj))
        print('t_obj: {}'.format(t_obj))
        out_kf = self.kf(x_obj,y_obj)
        # try:
        #     for i in range (len(x_obj)): 
        #     #tadinya drawing
        #         # cv2.line(frame, (x_obj[i],y_obj[i]), (x_obj[i+1],y_obj[i+1]), (255,255,255), 2) 
        # except:
        #     pass
        # save ke json
        config['output'] = {
            'object_detection': {
                'x_obj': x_obj,
                'y_obj': y_obj,
                't_obj': t_obj
            },
            'kalman_filter': out_kf
        }
        data_list[self.config_id] = config
        newSet().writeJson(data_list)
        # print('start writing')
        self.write_desc()
        # =============== end save
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