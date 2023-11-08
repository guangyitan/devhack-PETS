import numpy as np
import datetime
import cv2
from ultralytics import YOLO
from collections import deque

from deep_sort.deep_sort.tracker import Tracker
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection
from deep_sort.tools import generate_detections as gdet
from constants import FONT, FONT_WEIGHT, BOX_WEIGHT, CIRCLE_RADIUS

class TrafficDetection:
    def __init__(self):
        print("initializing traffic model...")
        # define some parameters
        self.conf_threshold = 0.5
        self.max_cosine_distance = 0.4
        self.nn_budget = None
        self.points = [deque(maxlen=32) for _ in range(1000)] # list of deques to store the points
        self.counter_A = 0
        self.counter_B = 0
        self.counter_C = 0
        self.start_line_A = (0, 480)
        self.end_line_A = (480, 480)
        self.start_line_B = (525, 480)
        self.end_line_B = (745, 480)
        self.start_line_C = (895, 480)
        self.end_line_C = (1165, 480)

        self.model = YOLO("model_files/yolov8s.pt")

        # define the class id car, motorcycle, bus, truck
        self.class_IDS = [2, 3, 5, 7]

        # Initialize the deep sort self.tracker
        model_filename = "model_files/mars-small128.pb"
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", self.max_cosine_distance, self.nn_budget)
        self.tracker = Tracker(metric)

        # load the COCO class labels the YOLO self.model was trained on
        classes_path = "model_files/parking_coco.txt"
        with open(classes_path, "r") as f:
            self.class_names = f.read().strip().split("\n")

        # create a list of random self.colors to represent each class
        np.random.seed(42)  # to get the same self.colors
        self.colors = np.random.randint(0, 255, size=(len(self.class_names), 3))  # (80, 3)
        print("traffic model initialized")

    def detect(self, frame):
        overlay = frame.copy()
        
        # draw the lines
        cv2.line(frame, self.start_line_A, self.end_line_A, (0, 255, 0), 12)
        cv2.line(frame, self.start_line_B, self.end_line_B, (255, 0, 0), 12)
        cv2.line(frame, self.start_line_C, self.end_line_C, (0, 0, 255), 12)
        
        # make the line transparent
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

        ############################################################
        ### Detect the objects in the frame using the YOLO self.model ###
        ############################################################

        # run the YOLO self.model on the frame
        # results = self.model(frame)
        results = self.model.predict(frame, classes = self.class_IDS)

        # loop over the results
        for result in results:
            # initialize the list of bounding boxes, confidences, and class IDs
            bboxes = []
            confidences = []
            class_ids = []

            # loop over the detections
            for data in result.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = data
                x = int(x1)
                y = int(y1)
                w = int(x2) - int(x1)
                h = int(y2) - int(y1)
                class_id = int(class_id)

                # filter out weak predictions by ensuring the confidence is
                # greater than the minimum confidence
                if confidence > self.conf_threshold:
                    bboxes.append([x, y, w, h])
                    confidences.append(confidence)
                    class_ids.append(class_id)
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
        ############################################################
        ### Track the objects in the frame using DeepSort        ###
        ############################################################

        # get the names of the detected objects
        names = [self.class_names[class_id] for class_id in class_ids]

        # get the features of the detected objects
        features = self.encoder(frame, bboxes)
        # convert the detections to deep sort format
        dets = []
        for bbox, conf, class_name, feature in zip(bboxes, confidences, names, features):
            dets.append(Detection(bbox, conf, class_name, feature))

        # run the self.tracker on the detections
        self.tracker.predict()
        self.tracker.update(dets)

        # loop over the tracked objects
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue

            # get the bounding box of the object, the name
            # of the object, and the track id
            bbox = track.to_tlbr()
            track_id = track.track_id
            class_name = track.get_class()
            # convert the bounding box to integers
            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

            # get the color associated with the class name
            class_id = self.class_names.index(class_name)
            color = self.colors[class_id]
            B, G, R = int(color[0]), int(color[1]), int(color[2])

            # draw the bounding box of the object, the name
            # of the predicted object, and the track id
            # text = str(track_id) + " - " + class_name
            text = class_name
            cv2.rectangle(frame, (x1, y1), (x2, y2), (B, G, R), BOX_WEIGHT) # obj bounding box
            cv2.rectangle(frame, (x1 - 1, y1 - 20), (x1 + len(text) * 12, y1), (B, G, R), -1) # box for class name
            cv2.putText(frame, text, (x1 + 5, y1 - 8), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)
            
            ############################################################
            ### Count the number of vehicles passing the lines       ###
            ############################################################
            
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            # append the center point of the current object to the self.points list
            self.points[track_id].append((center_x, center_y))

            cv2.circle(frame, (center_x, center_y), CIRCLE_RADIUS, (B, G, R), -1)
            
            # loop over the set of tracked self.points and draw them
            for i in range(1, len(self.points[track_id])):
                point1 = self.points[track_id][i - 1]
                point2 = self.points[track_id][i]
                # if the previous point or the current point is None, do nothing
                if point1 is None or point2 is None:
                    continue
                
                # line for object motion
                # cv2.line(frame, (point1), (point2), (0, 255, 0), 2)
                
            # get the last point from the self.points list and draw it
            last_point_x = self.points[track_id][0][0]
            last_point_y = self.points[track_id][0][1]
            # plot last point for motion
            # cv2.circle(frame, (int(last_point_x), int(last_point_y)), 4, (255, 0, 255), -1)    

            # if the y coordinate of the center point is below the line, and the x coordinate is 
            # between the start and end self.points of the line, and the the last point is above the line,
            # increment the total number of cars crossing the line and remove the center self.points from the list
            if center_y > self.start_line_A[1] and self.start_line_A[0] < center_x < self.end_line_A[0] and last_point_y < self.start_line_A[1]:
                self.counter_A += 1
                self.points[track_id].clear()
            elif center_y > self.start_line_B[1] and self.start_line_B[0] < center_x < self.end_line_B[0] and last_point_y < self.start_line_A[1]:
                self.counter_B += 1
                self.points[track_id].clear()
            elif center_y > self.start_line_C[1] and self.start_line_C[0] < center_x < self.end_line_C[0] and last_point_y < self.start_line_A[1]:
                self.counter_C += 1
                self.points[track_id].clear()
                
        ############################################################
        ### Some post-processing to display the results          ###
        ############################################################
        
        # draw the total number of vehicles passing the lines
        cv2.putText(frame, "A", (10, 483), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)
        cv2.putText(frame, "B", (530, 483), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)
        cv2.putText(frame, "C", (910, 483), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)
        cv2.putText(frame, f"{self.counter_A}", (270, 483), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)
        cv2.putText(frame, f"{self.counter_B}", (620, 483), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)
        cv2.putText(frame, f"{self.counter_C}", (1040, 483), FONT, 0.5, (255, 255, 255), FONT_WEIGHT)

        return frame