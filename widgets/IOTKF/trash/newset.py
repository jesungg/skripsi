import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty

#uix lib
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

#other lib
import os
from plyer.facades import FileChooser

#kv filepath
#kv = Builder.load_file("newset.kv")

#8 screen, 4 popup
#all screen -> pass (if empty as placeholder)

class welcomeScr(Screen): #1
    pass
class selVidScr(Screen): #2
    pass
        
class openFileDiag(FloatLayout): #pop1
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class chooseSet(Screen): #3
    pass
class newSet(Screen): #4
    pass
class cNoise(FloatLayout): #pop2
    pass
class addAct(FloatLayout): #pop3
    pass
class loadingScr(Screen): #5
    pass
class resultScr(Screen): #6
    pass
class resultVid(FloatLayout): #pop4
    pass
class aboutScr(Screen):
    pass
class helpScr(Screen):
    pass

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




#super: App
class newsetApp(App):
    def build(self):
        return scrMg

if __name__ == '__main__':
    newsetApp().run()