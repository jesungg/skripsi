from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

from sys import argv
from selectvideo import *
from main2 import *
import os
import fnmatch
import ctypes

#declare
class CheckNoise(FloatLayout):
    #popup show 2 video prepro(L) & frame(R)
    done = ObjectProperty(None)

class notRoot(FloatLayout):
    #check noise

    #input noise
    horizontal = ObjectProperty(None)
    vertical = ObjectProperty(None)
    noise_coord = ObjectProperty(None)

    #actions
    act_name = ObjectProperty(None)
    x0_coord = ObjectProperty(None)
    x1_coord = ObjectProperty(None)
    save_btn = ObjectProperty(None)
    
    #add more

class VideoSetup(App):
    def build(self):
        pass
    


if __name__ == '__main__':
    VideoSetup().run()