from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class HomeScreen(Widget):
    pass

class HomeApp(App):

    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    HomeApp().run()