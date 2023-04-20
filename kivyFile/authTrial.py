import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyC1cBc7jJrLVZrdSoTS3E-_VoSCwuHmbck",
  "authDomain": "projecttafix-4b39d.firebaseapp.com",
  "databaseURL": "https://projecttafix-4b39d-default-rtdb.firebaseio.com",
  "projectId": "projecttafix-4b39d",
  "storageBucket": "projecttafix-4b39d.appspot.com",
  "messagingSenderId": "258423894998",
  "appId": "1:258423894998:web:2f7c011ed039f6b3ffea77",
  "measurementId": "G-PSTWEKK57X",
  }

firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

# #AuthLogin
# email = input("Email: ")
# password = input("Password: ")
# try:
#     auth.sign_in_with_email_and_password(email,password) #to login w/ email&pass
#     print("succesfully log in")
# except:
#     print("Wrong Password")

#SignUp

# auth.create_user_with_email_and_password(email,password)
# print("SignUp Success")

data = {"nama": "Aya", "angkatan":"2019","jurusan":"IBM","jumlah_kp":"153"}
data_1 = {"nama": "Dayu", "angkatan":"2020","jurusan":"VCD","jumlah_kp":"148"}
# db.child("users").child("mahasiswa2").set(data_1)

aya = db.child("users").child("mahasiswa1").get()
dayu = db.child("users").child("mahasiswa2").get()
print(aya.val())
print(dayu.val())