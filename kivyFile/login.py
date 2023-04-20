from firebase import firebase

firebase = firebase.FirebaseApplication('https://projecttafix-4b39d-default-rtdb.firebaseio.com/', None)

data = {
    'Email':'Reiiiiii@gmail.com',
    'Password':'test1234',
    'Jurusan':'PSY',
    'Poin_kp':'281',
    'Plat_no':'L3727BJ'
}

# result = firebase.post('https://projecttafix-4b39d-default-rtdb.firebaseio.com/Mahasiswa', data)
# print(result)

#Get  Data
result = firebase.get('https://projecttafix-4b39d-default-rtdb.firebaseio.com/Mahasiswa', '')
print(result)

for i in result.keys():
    print(result[i]['Password'])