import cv2                # cv2 is used for Image and video processing,Computer vision applications,Real-time video processing and Cross-platform compatibility
import torch              # torch is used for Neural networks,GPU acceleration,Integration with other libraries and Research and development
import numpy as np        # numpy is used for Array operations,Data analysis,Mathematical Functions and also for speed

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)        #loads the YOLOv5s model from the Ultralytics repository using the PyTorch Hub API
# Define a function to remove noise from each frame
def remove_noise(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply a bilateral filter to smooth out noise while preserving edges
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    return denoised

cap = cv2.VideoCapture('cctv.mp4')           #reads frames from the video file named "cctv.mp4"
cv2.namedWindow('FRAME')#creates a new window with the title "FRAME" using the OpenCV library.This window will be used to display the frames from the video
while True:             #reads frames from the video file using the cap.read() method.This method returns two values: a boolean value indicating whether a frame was successfully read (ret), and the actual frame data (frame)              
    ret, frame = cap.read()
    if not ret:         # checks whether ret is False, indicating that there are no more frames to read from the video file. If there are no more frames, the loop is broken and the program exits
        break

    # Remove noise from the frame
    denoised = remove_noise(frame)
    # Resize the denoised frame
    resized = cv2.resize(denoised, (1020, 500))                   #This step is performed to ensure that the frame is of a consistent size for processing by the YOLOv5 model
    # Perform object detection on the resized frame using YOLOv5
    results = model(resized)
    # Render the detection results on the original frame
    frame = np.squeeze(results.render())   # is used to remove any dimensions of size 1 from the array.This step is performed to ensure that the resulting image has the correct shape for display using OpenCV

    cv2.imshow('FRAME', frame)      #displays the processed video frame in a new window with the title "FRAME"
    if cv2.waitKey(1) & 0xFF == 27: # waits for a key event for 1 millisecond. If the key event is the "Esc" key (key code 27), the program breaks out of the while loop and proceeds to release the video capture object and destroy all OpenCV windows
        break

cap.release()             # releases the video capture object created earlier using cv2.VideoCapture(). This is an important step to free up system resources and prevent memory leaks
cv2.destroyAllWindows()   #  destroys all OpenCV windows created during the execution of the program
