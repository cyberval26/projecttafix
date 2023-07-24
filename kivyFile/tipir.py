import pyrebase
import requests

import config

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty


firebaseConfig = {
  "apiKey": "AIzaSyC1cBc7jJrLVZrdSoTS3E-_VoSCwuHmbck",
  "authDomain": "projecttafix-4b39d.firebaseapp.com",
  "databaseURL": "https://projecttafix-4b39d-default-rtdb.firebaseio.com",
  "projectId": "projecttafix-4b39d",
  "storageBucket": "projecttafix-4b39d.appspot.com",
  "messagingSenderId": "258423894998",
  "appId": "1:258423894998:web:2f7c011ed039f6b3ffea77",
  "measurementId": "G-PSTWEKK57X"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

Window.size = (310,580)

# global variables
current_user = None
current_user_data = None

class main(MDApp):
    uid = None
    screen_manager = ScreenManager()
    
    def on_enter(self, *args):
        self.uid = args[1].get('uid')
        
    def build(self):
        # screen_manager.add_widget(Builder.load_file("pre-splash.kv"))
        self.screen_manager.add_widget(Builder.load_file("main.kv"))
        self.screen_manager.add_widget(Builder.load_file("home.kv"))
        self.screen_manager.add_widget(Builder.load_file("login.kv"))
        self.screen_manager.add_widget(Builder.load_file("signup.kv"))
        Builder.load_file('profile.kv')
        self.screen_manager.add_widget(ProfileScreen(name='profile'))
        return self.screen_manager
    
    def signup(self, email:str, password:str, nim:str, nopol:str, poinkp:str):
        global current_user, current_user_data
        try:
            user = auth.create_user_with_email_and_password(email, password)
            current_user = user
            print(current_user, nim, nopol,poinkp)
            db.child("mahasiswa").child(current_user['localId']).set({
                'nim': nim,
                'nopol': nopol,
                'poinkp': poinkp
            })
            current_user_data = {
                'nim': nim,
                'nopol': nopol,
                'poinkp': poinkp
            }
            self.root.current = 'home'
        except requests.exceptions.HTTPError:
            print('Failed to create user')

    def login(self, email, password):
        global current_user, current_user_data
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            current_user = user
            current_user_data = dict(db.child("mahasiswa").child(current_user['localId']).get().val())
            print(current_user_data)
            self.root.current = 'home'
        except requests.exceptions.HTTPError:
            print('Invalid email or password')

    def sign_out(self):
        self.root.current = 'login'

class ProfileScreen(MDScreen):
    email_label = ObjectProperty()
    nim_label = ObjectProperty()
    nopol_label = ObjectProperty()
    poinkp_label = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        # print(current_user)
        # print(current_user_data)
        self.email_label.text = current_user['email']
        self.nim_label.text = current_user_data['nim']
        self.nopol_label.text = current_user_data['nopol']
        self.poinkp_label.text = current_user_data['poinkp'] 
            

class InfoScreen(MDScreen):
    email_label = ObjectProperty()
    nim_label = ObjectProperty()
    nopol_label = ObjectProperty()
    poinkp_label = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        pass
            
if __name__ == '__main__':
    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'systemanddock')
    Config.set('kivy', 'keyboard_layout', 'numeric.json')
    Config.set('kivy', 'keyboard_provider', 'kivy')

    main().run()