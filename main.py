import cv2                         # cv2 is used for Image and video processing,Computer vision applications,Real-time video processing and Cross-platform compatibility
import torch                       # torch is used for Neural networks,GPU acceleration,Integration with other libraries and Research and development
from tracker import *              # imports everything from the tracker Module
import numpy as np                 # numpy is used for Array operations,Data analysis,Mathematical Functions and also for speed
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)        #loads the YOLOv5s model from the Ultralytics repository using the PyTorch Hub API

cap=cv2.VideoCapture('cctv.mp4')            #reads frames from the video file named "cctv.mp4"
#The below line defines a new function called POINTS that takes five parameters: event, x, y, flags, and param.This function will be called whenever a mouse event occurs in an OpenCV window
def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  # this line checks if the mouse event that occurred is a mouse move event. If so, the code inside the if statement will be executed.
        colorsBGR = [x, y]             # the x and y coordinates correspond to the pixel location in the image where the mouse pointer is currently located.
        print(colorsBGR)
        
cv2.namedWindow('FRAME')               #creates a new window with the title "FRAME" using the OpenCV library.This window will be used to display the frames from the video
#lets the mouse callback function for the window named 'FRAME' to be the function POINTS. Whenever a mouse event occurs in the 'FRAME' window, the function POINTS will be called, and the x and y coordinates of the mouse pointer will be printed to the console
cv2.setMouseCallback('FRAME', POINTS)  

tracker = Tracker()                # uses the Tracker class to track objects in the video or image sequence.
while True:
    ret,frame=cap.read(700) #this can be useful in cases where you want to start processing a video from a specific frame, or skip some frames at the beginning of a video that are not relevant to your analysis.
    frame=cv2.resize(frame,(1020,500))      #This step is performed to ensure that the frame is of a consistent size for processing by the YOLOv5 model
    results=model(frame)                    # Perform object detection on the resized frame using YOLOv5
    frame=np.squeeze(results.render())      # is used to remove any dimensions of size 1 from the array.This step is performed to ensure that the resulting image has the correct shape for display using OpenCV
 
    cv2.imshow('FRAME',frame)    #displays the processed video frame in a new window with the title "FRAME"
    if cv2.waitKey(1)&0xFF==27:  # waits for a key event for 1 millisecond. If the key event is the "Esc" key (key code 27), the program breaks out of the while loop and proceeds to release the video capture object and destroy all OpenCV windows
        break
cap.release()                  # releases the video capture object created earlier using cv2.VideoCapture(). This is an important step to free up system resources and prevent memory leaks
cv2.destroyAllWindows()        #  destroys all OpenCV windows created during the execution of the program 
    
    
