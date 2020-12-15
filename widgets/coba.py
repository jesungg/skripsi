import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        padding: [2,2,2,2]
        spacing: 2
        orientation: 'vertical'
        Label:
            font_size: 70
            text: "Title"
        Label:
            font_size: 50
            text: "Details"
        Button:
            pos_hint: {'center_x': .5, 'center_y': .5}
            size_hint: None, None
            size: 140,50
            size_hint: .1, .1
            text: "start"
            on_press: root.manager.current = 'start'
<StartScreen>:
    BoxLayout:
        padding: [2,2,2,10]
        spacing: 2
        orientation: 'vertical'
        Label:
            font_size: 70
            text: "Title2"
        Label:
            font_size: 50
            text: "Details2"
        Button:
            pos_hint: {'center_x': .5, 'center_y': .5}
            size_hint: None, None
            size: 140,50
            size_hint: .1, .1
            text: "home"
            on_press: root.manager.current = 'home'
""")

class HomeScreen(Screen):
    pass

class StartScreen(Screen):
    pass

#create
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(StartScreen(name='start'))

class MainnApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MainnApp().run()
