from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from firebase_admin import db
import requests
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

cred = credentials.Certificate('kivyFile/privateKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projecttafix-4b39d-default-rtdb.firebaseio.com/'
})

# Builder.load_file("home.kv")

# # Get a database client
# database_url = 'https://projecttafix-4b39d-default-rtdb.firebaseio.com/'
# ref = db.reference('/', url=database_url)

Window.size = (310,580)

class Main(MDApp):
    uid = None
    
    def on_enter(self, *args):
        self.uid = args[1].get('uid')
        
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        # screen_manager.add_widget(Builder.load_file("pre-splash.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("home.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(ProfileScreen(name='profile'))
        self.set_current_user(screen_manager)
        return screen_manager
    
    def set_current_user(self, screen_manager):
        # set current user on screen manager
        current_user = auth.create_user()
        screen_manager.current_user = current_user
    
    def send_data(self, email, password):
        # Get a reference to the Mahasiswa node in the database
        mahasiswa_ref = db.reference('Mahasiswa')
        # Query the database to get the user node with the specified email
        query = mahasiswa_ref.order_by_child('Email').equal_to(email)
        user_nodes = query.get()
        # Check if a user node with the specified email exists
        if not user_nodes:
            print('User not found')
            return
        # Get the first user node (assuming only one user with the specified email)
        user_node_key = list(user_nodes.keys())[0]
        user_node = user_nodes[user_node_key]
        # Check if the password matches
        if user_node['Password'] != password:
            print('Incorrect password')
            return
        print(user_node_key, user_node)
        # Set the current screen to the home screen
        self.root.current = 'home'
    
    def on_start(self):
        # Get a reference to the database
        db_ref = db.reference('Mahasiswa')
        # Get the data from the database
        data = db_ref.get()
        # # Update the text of the label widget with the data
        home_screen = self.root.get_screen('home')
        if 'data_label' in home_screen.ids:
            home_screen.ids.data_label.text = str(data)

    
    def sign_out(self, uid):
        try:
            # Use the uid variable instead of user
            auth.revoke_refresh_tokens(uid)
            print("User logged out")
            self.root.current = 'login'
        except Exception as e:
            print("Logout failed:", e)
            # Display error message here, if desired

class ProfileScreen(Screen):
    def on_pre_enter(self):
        # Get a reference to the Mahasiswa node in the database
        mahasiswa_ref = db.reference('Mahasiswa')
        # Get the user's data from the database
        user_data = mahasiswa_ref.child(self.manager.current_user.uid).get()
        print(f"current uid: {self.manager.current_user.uid} | user_data: {user_data}")
        # Display the user's data on the screen
        self.ids.nama_label.text = user_data['Nama']
        self.ids.email_label.text = user_data['Email']
        self.ids.jurusan_label.text = user_data['Jurusan']
        self.ids.nopol_label.text = user_data['Plat_no']
        self.ids.poin_label.text = user_data['Poin_kp']
    
            
if __name__ == '__main__':

    # cred = firebase_admin.credentials.Certificate("path/to/serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'systemanddock')
    Config.set('kivy', 'keyboard_layout', 'numeric.json')
    Config.set('kivy', 'keyboard_provider', 'kivy')

    Main().run()