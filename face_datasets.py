# Import OpenCV2 for image processing
import cv2
#import sys
import time
#import RPi.GPIO as gpio
from picamera.array import PiRGBArray
from picamera import PiCamera
#import imutils
import numpy as np
# Start capturing video
d = 300
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
# Detect object in video stream using Haarcascade Frontal Face
#face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



# For each person, one face id
face_id = 8888

# Initialize sample face image
count = 0

# Start looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # Capture video frame
    #image_frame = imutils.resize(f.array, width=320)
    image = frame.array
    # Convert frame to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.resize(image,(750,750), interpolation = cv2.INTER_AREA)
    sizeIm = image.shape

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect frames of different sizes, list of faces rectangles
    faces = face_cascade.detectMultiScale(image, 1.3, 5)

    # Loops for each faces
    for (x,y,w,h) in faces:

        # Crop the image frame into rectangle
        cv2.rectangle(image, (x,y), (x+w,y+h), (255,255,255), 2)
        #roi_gray = image[y:y+h, x:x+w]
        # Increment sample face image
        count+=1

        # Save the captured image into the datasets folder
        
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", image[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
    cv2.imshow("frame", image)
    key = cv2.waitKey(1) & 0xFF
    # To stop taking video, press 'q' for at least 100ms
#if cv2.waitKey(1) & 0xFF == ord('q'):
        #break
    rawCapture.truncate(0) 
    
    # If image taken reach 100, stop taking video
    if key == ord("q"):
        break

    if count >= 100:
        break
# Stop video
#camera.close()

# Close all started windows
#cv2.destroyAllWindows()
