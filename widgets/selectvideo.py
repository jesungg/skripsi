from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


from sys import argv
import main2
from main2 import HomeScreen, sm
import videosetup
import os
import fnmatch
import ctypes

#declare
class EmptyScreen(Screen):
    pass

class SelectDialog(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    stringnya = ObjectProperty(None)

    def move_to_newsetup(self):
        sm.switch_to(HomeScreen(), direction='left')

    def dismiss_popup(self):
        print("close popup")
        self._popup.dismiss()

    def show_file(self):
        print("show popup")
        content = SelectDialog(select=self.select, cancel=self.dismiss_popup)
        self._popup =Popup(title="Select video file", content=content, size_hint=(.9, .9))
        self._popup.open()

    def select(self, dirpath, filepath):
        #print('path', dirpath,type(dirpath))
        #print('filename', filepath, type(filepath))
        stringnya = str(filepath)
        acceptedformat = 'mp4'
        if stringnya[-3:] == acceptedformat:
            print("acceptedformat")
            pass
        else:
            print("not accepted")
            stringnya = None
        #print('stringnya', stringnya, type(stringnya))
        return stringnya
        #self.dismiss_popup()


        
    def run(self):
        run = videosetup.VideoSetup().run()


    try:
        if stringya is None:
            pass
    except:
        pass



class SelectVideo(App):
    def build(self):
        pass            
            

Factory.register('Root', cls=Root)
Factory.register('SelectDialog', cls=SelectDialog)

if __name__ == '__main__':
    SelectVideo().run()