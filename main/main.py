from pothole_detection import PotholeDetection
from accident_detection import AccidentDetection
from parking_detection import ParkingDetection
from traffic_detection import TrafficDetection
import cv2
import os

pothole_detection = PotholeDetection()
accident_detection = AccidentDetection()
parking_detection = ParkingDetection()
traffic_detection = TrafficDetection()

file_name = 'accident-pothole-demo'
# file_name = 'accident-pothole-demo2'
# file_name = 'pothole-demo'
# file_name = 'pothole-demo2'
# file_name = 'traffic-pothole-demo'
# file_name = 'parking-demo'

#defining the video source (0 for camera or file name for video)
# cap = cv2.VideoCapture(0) 
cap = cv2.VideoCapture(f'../media/{file_name}.mp4') 
frame_rate = cap.get(cv2.CAP_PROP_FPS)

frame_width  = cap.get(3)
frame_height = cap.get(4)
# output = cv2.VideoWriter(f'output/{file_name}.avi', cv2.VideoWriter_fourcc(*'MJPG'), frame_rate,(int(frame_width),int(frame_height)))
output = cv2.VideoWriter(os.getcwd() + f'/output/{file_name}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (int(frame_width), int(frame_height)))

while True:
    ret, frame = cap.read()
    if ret == False:
        break

    # comment / uncomment related lines for needed detection
    frame = accident_detection.detect(frame)
    frame = pothole_detection.detect(frame)
    # frame = parking_detection.detect(frame)
    # frame = traffic_detection.detect(frame)

    #showing and saving result
    cv2.imshow('frame', frame)
    output.write(frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the video capture object and output video writer
cap.release()
output.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()