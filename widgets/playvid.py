import os
os.environ['KIVY_VIDEO'] = 'gstreamer'

import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.video import Video

from kivy.uix.floatlayout import FloatLayout

class VideoScreen(FloatLayout):
    try:
        video = Video(source='vtest.avi', state='play')
        print(video.loaded())
    except:
        pass

class Videoo(App):

    def build(self):
        return VideoScreen()

if __name__ == '__main__':
    Videoo().run()
