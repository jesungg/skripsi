from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

from sys import argv
import os
import fnmatch

class SelectDialog(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        print("close popup")
        self._popup.dismiss()

    def show_file(self):
        print("show popup")
        content = SelectDialog(select=self.select, cancel=self.dismiss_popup)
        self._popup =Popup(title="Select video file", content=content, size_hint=(.9, .9))
        self._popup.open()

    def select(self, dirpath, filepath):
        print('path', dirpath,type(dirpath))
        print('filename', filepath, type(filepath))
        stringnya = str(filepath)
        print('stringnya', stringnya, type(stringnya))
        self.dismiss_popup()

class OpenFile(App):
    pass

Factory.register('Root', cls=Root)
Factory.register('SelectDialog', cls=SelectDialog)

if __name__ == '__main__':
    OpenFile().run()