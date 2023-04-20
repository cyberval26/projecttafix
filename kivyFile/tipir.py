from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
# from firebase_admin import db

# import firebase_admin
# from firebase_admin import auth

# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate('D:/projecttafix/privateKey.json')
# firebase_admin.initialize_app(cred)

# # Get a database client
# database_url = 'https://projecttafix-4b39d-default-rtdb.firebaseio.com/'
# ref = db.reference('/', url=database_url)

Window.size = (310,580)

class Main(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        # screen_manager.add_widget(Builder.load_file("pre-splash.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("home.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        # screen_manager.add_widget(Builder.load_file("alert.kv"))
        return screen_manager
    
    def send_data(self, email, password):
        from firebase import firebase  
        firebase = firebase.FirebaseApplication('https://projecttafix-4b39d-default-rtdb.firebaseio.com/', None)
        #Get  Data
        result = firebase.get('https://projecttafix-4b39d-default-rtdb.firebaseio.com/Mahasiswa', '')
        print(result)

        for i in result.keys():
            if result[i]['Email']== email:
                if result[i]['Password'] == password:
                    print(email+" Logged In!")
                    self.root.current = 'home'
    
    # def on_start(self):
    #     # Get a reference to the database
    #     db_ref = db.reference('https://projecttafix-4b39d-default-rtdb.firebaseio.com/Mahasiswa')
    #     # Get the data from the database
    #     data = db_ref.get()
    #     # Update the text of the label widget with the data
    #     self.root.get_screen('home').ids.data_label.text = str(data)
    
    # def sign_out(self, uid):
    #     auth.revoke_refresh_tokens(uid)
    #     print("User logged out")
    #     self.root.current = 'login'

if __name__ == '__main__':

    # cred = firebase_admin.credentials.Certificate("path/to/serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'systemanddock')
    Config.set('kivy', 'keyboard_layout', 'numeric.json')
    Config.set('kivy', 'keyboard_provider', 'kivy')

    Main().run()
