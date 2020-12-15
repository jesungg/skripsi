import kivy  # Required to run Kivy such as the next line of code
kivy.require('1.9.1')  # used to alert user if this code is run on an earlier version of Kivy.
from kivy.app import App  # Imports the base App class required for Kivy Apps
from kivy.lang import Builder  # Imports the KV language builder that provides the layout of kivy screens
from kivy.uix.screenmanager import ScreenManager, Screen  # Imports the Kivy Screen manager and Kivys Screen class
 
Builder.load_string(""" # String that will build all four Kivy screens.
<WelcomeScreen>: # Identifies layout/interactivity for the WelcomeScreen.
    GridLayout: # Creates a GridLayout for WelcomeScreen.
        cols: 1 # Sets column property to 1.
        Label: # Creates a Label Widget instance.
            text: "You're On The Welcome Screen. Please Select Which Screen You Want To Go To" # Sets above Label text property
        Button: # Creates a Button Widget instance.
            text: 'Appetizers' #  Sets above button text property
            on_release:
                # on_release is a Kivy mouse release event.
                root.manager.transition.direction = 'right' # Sets screen transition movement to right.
                root.manager.current = 'appetizer_screen' # Switches Kivy GUI screen to screen one.
        Button: # Creates a Button Widget instance.
            text: 'Switch To Screen Two' #  Sets above button text property
            on_release:
                # on_release is a Kivy mouse release event.
                root.manager.transition.direction = 'right' # Sets screen transition movement to right.
                root.manager.current = 'screen_two' # Switches Kivy GUI screen to screen two.
        Button: # Creates a Button Widget instance.
            text: 'Switch To Screen Three' #  Sets above button text property
            on_release:
                # on_release is a Kivy mouse release event.
                root.manager.transition.direction = 'right' # Sets screen transition movement to right.
                root.manager.current = 'screen_three' # Switches Kivy GUI screen to screen three.
<AppetizerScreen>: # Identifies layout/interactivity for the AppetizerScreen.
    GridLayout: # Creates a GridLayout for the entire appetizer GUI screen
        cols: 1 # Sets column property to 1.
        Label: # Creates a Label Widget instance for first row of GUI.
            text: 'Please Select Both A First And Second Appetizer' # Text for above Label.
        Label: # Creates a Label Widget instance for second row of GUI.
            text: 'First Appetizer Selection' # Text for above Label.
            id: first_app
            color: 1,1,1,1 # Sets text colour to black.
            canvas.before:
                Color: # Six lines of code (starting above) set Label background colour
                    rgba: 0.3, 0.3, 0.3,.6 # Colour code
                Rectangle:
                    pos: self.pos # required to position rectangle inside of Label widget.
                    size: self.size
        GridLayout: # Creates nested 2 column GridLayout on Row 3 of GUI.
            cols: 2 # Sets nested GridLayout to 2 columns.
            Label: # Creates a Label Widget in first column of nested GridLayout.
                text: 'Oysters On The Half' # Text for above Label.
            Button: # Creates a Button Widget in Second column of nested GridLayout.
                text: 'Please Select By Clicking Here' # Text for above Button.
                on_release:
                    # on_release is a Kivy mouse release event
                    root.oyster_selected() # Calls oyster_selected event handler class.
        Label: # Creates a Label Widget instance for fourth row of GUI.
            text: 'Or' # Text for above Label.
        GridLayout: # Creates nested 2 column GridLayout on Row 5 of GUI.
            cols: 2 # Sets nested GridLayout to 2 columns.
            Label: # Creates a Label Widget in first column of nested GridLayout.
                text: 'Smoked Pork Belly On Apple Butter\\nWith Baby Organic Kale Bourbon Glazed Pecans' # Text for above Label.
                halign: 'center' # Sets text horizontal alignment to cenre of button.
            Button: # Creates a Button Widget in Second column of nested GridLayout.
                text: 'Please Select By Clicking Here' # Text for above Button.
                on_release:
                    # on_release is a Kivy mouse release event
                    root.pork_belly_selected() # Calls pork_belly_selected event handler class.
        Label: # Creates a Label Widget instance for 6th row of GUI.
            text: 'Second Appetizer Selection' # Text for above Label.
            id: second_app
            canvas.before:
                Color: # Six lines of code (starting above) set Label background colour
                    rgba: 0.3, 0.3, 0.3,.6 # Colour code
                Rectangle:
                    pos: self.pos # required to position rectangle inside of Label widget.
                    size: self.size
        GridLayout: # Creates nested 2 column GridLayout on Row 7 of GUI.
            cols: 2 # Sets nested GridLayout to 2 columns.
            Label: # Creates a Label Widget in first column of nested GridLayout.
                text: 'Pan Seared Sea Scallop\\nCreamy Corn Grits With Sweet Pea Emulsion,\\nFried Crisp Leeks, Balsamic Drizzle' # Text for above Label.
                halign: 'center' # Sets text horizontal alignment to cenre of button.
            Button: # Creates a Button Widget in Second column of nested GridLayout.
                text: 'Please Select By Clicking Here' # Text for above Button.
                on_release:
                    # on_release is a Kivy mouse release event
                    root.scallop_selected() # Calls scallop_selected event handler class.
        Label: # Creates a Label Widget instance for 8th row of GUI.
            text: 'Or' # Text for above Label.
        GridLayout: # Creates nested 2 column GridLayout on Row 9 of GUI.
            cols: 2 # Sets nested GridLayout to 2 columns.
            Label: # Creates a Label Widget in first column of nested GridLayout.
                text: 'Craw Fish Bisque En Croute' # Text for above Label.
            Button: # Creates a Button Widget in Second column of nested GridLayout.
                text: 'Please Select By Clicking Here' # Text for above Button.
                on_release:
                    # on_release is a Kivy mouse release event
                    root.crawfish_selected() # Calls crawfish_selected event handler class.
        Button: # Creates a Button Widget instance on row 10 of GUI.
            text: "Return To Menu Welcome Screen By Clicking Here" #  Sets above button text property
            background_normal: "" # Button background defalts to grey. This sets the background to plain.
            background_color: (0.3, 0.3, 0.3,.6) # Sets Button background colour.
            on_release:
                # on_release is a Kivy mouse release event
                root.manager.transition.direction = 'right' # Sets screen transition movement to right.
                root.manager.current = 'welcome_screen' # Switches Kivy GUI screen to the welcome screen.
<SecondScreen>: # Identifies layout/interactivity for the SecondScreen.
    GridLayout: # Creates a GridLayout for SecondScreen.
        cols: 1 # Sets column property to 1.
        Button: # Creates a Button Widget instance.
            text: "You're On Screen Two. Press To Return To Welcome Screen" #  Sets above button text property
            on_release:
                # on_release is a Kivy mouse release event
                root.manager.transition.direction = 'right' # Sets screen transition movement to right.
                root.manager.current = 'welcome_screen' # Switches Kivy GUI screen to the welcome screen.
<ThirdScreen>: # Identifies layout/interactivity for the ThirdScreen.
    GridLayout: # Creates a GridLayout for ThirdScreen.
        cols: 1 # Sets column property to 1.
        Button: # Creates a Button Widget instance.
            text: "You're On Screen Three. Press To Return To Welcome Screen" #  Sets above button text property
            on_release:
                # on_release is a Kivy mouse release event
                root.manager.transition.direction = 'right' # Sets screen transition movement to right.
                root.manager.current = 'welcome_screen' # Switches Kivy GUI screen to the welcome screen.
""")
 
class WelcomeScreen(Screen):  # Creates a WelcomeScreen widget from the above kv language data string.
    pass  # Python placeholder for class.
 
class AppetizerScreen(Screen):  # Creates a AppetizerScreen widget from the above kv language data string.
 
    def oyster_selected(self): # Kivy event handler for events/callbacks on AppetizerScreen
        print("Oyster Selected") # Prints to python console.
        self.ids.first_app.text = "First Appetizer Selection: Oysters On The Half" # Code to update appetizer choice on Label id'd as first_app.
 
    def pork_belly_selected(self): # Kivy event handler for events/callbacks on AppetizerScreen
        print("Pork Belly Selected") # Prints to python console.
        self.ids.first_app.text = "First Appetizer Selection: Smoked Pork Belly On Apple Butter" # Code to update appetizer choice on Label id'd as first_app.
 
    def scallop_selected(self): # Kivy event handler for events/callbacks on AppetizerScreen
        print("Scallop Selected") # Prints to python console.
        self.ids.second_app.text = "Second Appetizer Selection: Pan Seared Sea Scallop" # Code to update appetizer choice on Label id'd as second_app.
 
    def crawfish_selected(self): # Kivy event handler for events/callbacks on AppetizerScreen
        print("Crawfish Selected") # Prints to python console.
        self.ids.second_app.text = "Second Appetizer Selection: Craw Fish Bisque En Croute" # Code to update appetizer choice on Label id'd as second_app.
 
class SecondScreen(Screen):  # Creates a SecondScreen widget from the above kv language data string.
    pass  # Python placeholder for class.
 
class ThirdScreen(Screen):  # Creates a ThirdScreen widget from the above kv language data string.
    pass  # Python placeholder for class.
 
sm = ScreenManager()  # Creates an instance (copy) of ScreenManager as variable sm. ScreenManager switches between Screen Objects.
sm.add_widget(WelcomeScreen(
    name='welcome_screen'))  # Adds WelcomeScreen widget to ScreenManager. ScreenManager id's screen as welcome_screen.
sm.add_widget(AppetizerScreen(
    name='appetizer_screen'))  # Adds AppetizerScreen widget to ScreenManager. ScreenManager id's screen as appetizer_screen.
sm.add_widget(SecondScreen(
    name='screen_two'))  # Adds SecondScreen widget to ScreenManager. ScreenManager id's screen as screen_two.
sm.add_widget(ThirdScreen(
    name='screen_three'))  # Adds ThirdScreen widget to ScreenManager. ScreenManager id's screen as screen_three.
 
class SwitchingScreenApp(App):  # Creates the instance (copy) of the Kivy App class named SwitchingScreenApp
 
    def build(self):  # build is a method of Kivy's App class used to place widgets onto the GUI.
        return sm  # return calls the build method which in turn builds the GUI.
 
SwitchingScreenApp().run()  # Runs SwitchingScreenApp