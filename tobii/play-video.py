# importing libraries
import cv2
import time
import numpy as np

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('/home/janci/Documents/DIPLO/TRACKING/exp2/chunks-1-9.mp4')
# cap = cv2.VideoCapture('/home/janci/Documents/DIPLO/tracker-sample.mp4')
# cap = cv2.VideoCapture('/home/janci/Documents/DIPLO/scenevideo.mp4')
# cap = cv2.VideoCapture('/home/janci/Documents/DIPLO/PILOT/1 David Brandys/scenevideo-part-1.mp4')

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Read until video is completed
while cap.isOpened():

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        # sleep for 1/30 seconds
        # time.sleep(1/30)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()