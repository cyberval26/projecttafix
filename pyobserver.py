import os
from time import sleep
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore, storage

path = 'C:\\Users\\ASUS\\stream'

# ganti True kalau mau upload semua file csv ke firebase. ganti False kalau upload csv terakhir saja
upload_all = False

cred = credentials.Certificate(
    "projecttafix-4b39d-firebase-adminsdk-3b0o9-92666b36b4.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def list_csv():
    csv_files = [file for file in os.listdir(path) if file.endswith(".csv")]
    try:
        if upload_all:
            for csv_file in csv_files:
                parse_csv(csv_file)
        else:
            parse_csv(csv_files[-1])
    except Exception as e:
        print(e)

def parse_csv(file):
    df = pd.read_csv(f'{path}\\{file}')
    df = df[['timestamp', 'plate', 'file']]
    # print(df)
    upload_to_firebase(df.to_dict('records')) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html


def upload_to_firebase(dict_data):
    uploaded_something = False
    collection_ref = db.collection('plates')
    for data in dict_data:
        doc_id = f'{data["timestamp"]}{data["plate"]}'
        # firestore
        document_ref = collection_ref.document(doc_id)
        if data['timestamp'] != 'timestamp' and not document_ref.get().exists:
            # storage
            bucket = storage.bucket('projecttafix-4b39d.appspot.com')
            blob = bucket.blob(doc_id)
            blob.upload_from_filename(f'{path}\\{data["file"]}')
            blob.make_public()

            uploaded_something = True
            d = {
                'timestamp': data['timestamp'],
                'plate': data['plate'],
                'image_url': blob.public_url,
            }
            document_ref.set(d)


    if uploaded_something:
        print('Updates have been uploaded to firebase')


while True:
    # print('checking...')
    sleep(1)
    list_csv()

# list_csv()
