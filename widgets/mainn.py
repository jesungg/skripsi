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
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

#other lib
import os


#kv filepath
kv = Builder.load_file("mainn.kv")

#screen list
class HomeScreen(Screen):
    pass

class StartScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class HelpScreen(Screen):
    pass

class SettingScreen(Screen):
    pass


#screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(StartScreen(name='start'))
sm.add_widget(AboutScreen(name='about'))
sm.add_widget(HelpScreen(name='help'))
sm.add_widget(SettingScreen(name='setting'))

#select video widgets
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class selectvid(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_popup()
    
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select video file", content=content, size_hint=(.9, .9))
        self._popup.open()

#app gue
class Mainn(App):
    def build(self):
        return sm

if __name__ == '__main__':
    Mainn().run()
