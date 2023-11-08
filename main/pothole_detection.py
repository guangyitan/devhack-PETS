
#importing necessary libraries
import cv2
import time
import geocoder
import os
from constants import FONT_WEIGHT, FONT, BOX_WEIGHT

class PotholeDetection:
    def __init__(self):
        #reading label name from obj.names file
        self.class_name = []
        with open(os.path.join("model_files",'pothole_obj.names'), 'r') as f:
            self.class_name = [cname.strip() for cname in f.readlines()]

        #importing model weights and config file
        #defining the model parameters
        print("initializing pothole model...")
        self.net1 = cv2.dnn.readNet('model_files/pothole_yolov4_tiny.weights', 'model_files/pothole_yolov4_tiny.cfg')
        self.net1.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net1.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        self.model = cv2.dnn_DetectionModel(self.net1)
        self.model.setInputParams(size=(640, 480), scale=1/255, swapRB=True)
        print("pothole model initialized")

        #defining parameters for result saving and get coordinates
        #defining initial values for some parameters in the script
        self.g = geocoder.ip('me')
        self.result_path = "pothole_coordinates"
        self.starting_time = time.time()
        self.Conf_threshold = 0.5
        self.NMS_threshold = 0.4
        self.i = 0
        self.b = 0
        self.score_threshold = 0.3

    def detect(self, frame):
        #analysis the stream with detection model
        classes, scores, boxes = self.model.detect(frame, self.Conf_threshold, self.NMS_threshold)
        for (classid, score, box) in zip(classes, scores, boxes):
            frame_height, frame_width, _ = frame.shape
            label = "pothole"
            x, y, w, h = box
            recarea = w*h
            frame_area = frame_width*frame_height
            #drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
            if(len(scores)!=0 and scores[0]>=self.score_threshold):
                # if((recarea/frame_area)<=0.1 and box[1]<600):
                # text = "%" + str(round(scores[0]*100,2)) + " " + label
                text = label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,0), BOX_WEIGHT)
                cv2.rectangle(frame, (box[0] - 1, box[1] - 25), (box[0] + len(text) * 10, box[1]), (255, 255, 0), -1) # box for class name
                cv2.putText(frame, text, (box[0] + 5, box[1]-10), FONT, 0.5, (0, 0, 0), FONT_WEIGHT)
        return frame