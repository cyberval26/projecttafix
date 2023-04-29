import pyrebase
import requests

from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

# cred = credentials.Certificate('kivyFile/privateKey.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://projecttafix-4b39d-default-rtdb.firebaseio.com/'
# })

# Builder.load_file("home.kv")

# # Get a database client
# database_url = 'https://projecttafix-4b39d-default-rtdb.firebaseio.com/'
# ref = db.reference('/', url=database_url)

# config = {
#   "apiKey": "apiKey",
#   "authDomain": "projectId.firebaseapp.com",
#   "databaseURL": "https://databaseName.firebaseio.com",
#   "storageBucket": "projectId.appspot.com"
# }

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
        # Builder.load_file('profile_screen.kv')
        self.screen_manager.add_widget(Builder.load_file("main.kv"))
        self.screen_manager.add_widget(Builder.load_file("home.kv"))
        self.screen_manager.add_widget(Builder.load_file("login.kv"))
        self.screen_manager.add_widget(Builder.load_file("signup.kv"))
        self.screen_manager.add_widget(Builder.load_file("profile_screen.kv"))
        # self.screen_manager.add_widget(profile_screen(name='profile'))
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
    
    def on_start(self):
        pass

    
    def sign_out(self):
        pass

class profile_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email = ""
        self.nim = ""
        self.nopol = ""
        self.poinkp = ""

    def on_pre_enter(self):
        print(current_user)
        print(current_user_data)
        self.email = current_user['email']
        self.nim = current_user_data['nim']
        self.nopol = current_user_data['nopol']
        self.poinkp = current_user_data['poinkp']
        # # Get a reference to the Mahasiswa node in the database
        # mahasiswa_ref = db.reference('Mahasiswa')
        # # Get the user's data from the database
        # user_data = mahasiswa_ref.child(self.manager.current_user.uid).get()
        # print(f"current uid: {self.manager.current_user.uid} | user_data: {user_data}")
        # # Display the user's data on the screen
        # self.ids.nama_label.text = user_data['Nama']
        # self.ids.email_label.text = user_data['Email']
        # self.ids.jurusan_label.text = user_data['Jurusan']
        # self.ids.nopol_label.text = user_data['Plat_no']
        # self.ids.poin_label.text = user_data['Poin_kp']  
            
if __name__ == '__main__':
    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'systemanddock')
    Config.set('kivy', 'keyboard_layout', 'numeric.json')
    Config.set('kivy', 'keyboard_provider', 'kivy')

    main().run()