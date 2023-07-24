import cv2
import time
import datetime
import pyrebase
import pytesseract
# from firebase_admin import credentials
# from firebase_admin import db


cam = cv2.VideoCapture(0)

config = {
  "apiKey": "0G1yjOR7rC302LA9fUtRf3miZ4AORO4Xtx2PLokF",
  "authDomain": "projecttaiot.firebaseapp.com",
  "databaseURL": "https://projecttaiot-default-rtdb.firebaseio.com",
  "storageBucket": "projecttaiot.appspot.com"
}

# https://github.com/nhorvath/Pyrebase4
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

print("Send Data to Firebase Using Raspberry Pi")
print("----------------------------------------")
print()

# Initialize the OCR engine
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
tesseract_config = '--oem 1 --psm 6'

# Read the image from the camera
ret, image = cam.read()

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to the grayscale image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]



# Perform OCR on the thresholded image
text = pytesseract.image_to_string(thresh, config=tesseract_config)

# Send the extracted data to Firebase
data = {'text': text}
db.child('ocr_data').push(data)

# Set a counter for the captured images
counter = 0

while True:
    # Get the current time
    current_time = time.time()
    
    # Capture an image every 5 minutes (300 seconds)
    if current_time % 300 == 0:
        # Read the image from the camera
        ret, image = cam.read()
        
        # Check if an image was successfully read
        if ret:
            # Create a unique filename with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = '/home/pi/testimage.jpg'.format(timestamp)
            
            # Save the image with the unique filename
            cv2.imwrite(filename, image)
            
            # Upload the image file to Firebase Storage
            storage.child("images/{}".format(filename)).put(filename)
            
            # Increment the counter
            counter += 1
    
    # Show the image on the screen if available
    # if 'image' in locals():
    #     cv2.imshow('Imagetest',image)
    
    # Wait for a key press for 1 millisecond
    k = cv2.waitKey(1)
    
    # Exit the loop if a key is pressed
    if k != -1:
        break

# Release the camera and close all windows
cam.release()
cv2.destroyAllWindows()
