#GUI lib
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
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

from main2 import *
#other lib
import os


#kv filepath
kv = Builder.load_file("main2.kv")


#screen list
class MyScreenManager(ScreenManager):
    pass

class HomeScreen(Screen):
    def run(self):
        import selectvideo
        run = selectvideo.SelectVideo().run()
    pass

class StartScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class HelpScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

class NewSetupScreen(Screen):
    pass

     


#screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(StartScreen(name='start'))
sm.add_widget(AboutScreen(name='about'))
sm.add_widget(HelpScreen(name='help'))
sm.add_widget(SettingScreen(name='setting'))
sm.add_widget(NewSetupScreen(name='newsetup'))


#app gue
class Main2(App):
    def build(self):
        return sm
    
    
if __name__ == '__main__':
    Main2().run()
