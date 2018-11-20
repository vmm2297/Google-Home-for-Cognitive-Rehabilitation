# Import OpenCV2 for image processing
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
# Import numpy for matrices calculations
import numpy as np
import time
import pygame
d = 300
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)
# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the trained mode
recognizer.read('/home/pi/Raspberry-Face-Recognition-PiCamera/trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "/home/pi/Raspberry-Face-Recognition-PiCamera/haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture
#cam = cv2.VideoCapture(-1)

# Loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Read the video frame
    #ret, im = cam.read()
     
    image = frame.array
    # Convert the captured frame into grayscale
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #image = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # Get all face from the video frame
    faces = faceCascade.detectMultiScale(image, 1.3,5)
    #faces = faceCascade.detectMultiScale(image,1.2,5)
    # For each face in faces
    for(x,y,w,h) in faces:

        # Create rectangle around the face
        cv2.rectangle(image, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

        # Recognize the face belongs to which ID
        Id = recognizer.predict(image[y:y+h,x:x+w])

        # Check the ID if exist 
        
        if "9999" in str(Id):
            Id = "Hey Jerry remember to take medicine:)"
            
        #If not exist, then it is Unknown
        elif "8888" in str(Id):
            Id = "Dr.Moore check your calendar:)"
        else:
            Id = "Unknown"

        # Put text describe who is in the picture
        cv2.rectangle(image, (x-22,y-90), (x+w+22, y-22), (255,255,255), -1)
        cv2.putText(image, str(Id), (x,y-40), font,0.8, (0,0,0), 2)
        
    # Display the video frame with the bounded rectangle
    cv2.imshow("frame",image) 
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    # If 'q' is pressed, close program
    if key == ord('q'):
        break

# Stop the camera
#cam.release()

# Close all windows
#cv2.destroyAllWindows()
