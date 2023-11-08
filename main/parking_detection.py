import cv2
import pandas as pd
import numpy as np
import json
from ultralytics import YOLO
from constants import FONT_WEIGHT, FONT, BOX_WEIGHT, CIRCLE_RADIUS

class Slot:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.available = False

    def reset(self):
        self.available = True  # Set back to available

    def __getitem__(self, item):
         return getattr(self, item)

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'coordinates': self.coordinates,
            'available': self.available
        })

class ParkingDetection:
    def __init__(self):

        print("initializing parking model...")
        self.model = YOLO('model_files/yolov8s.pt')
        
        self.frame_nmr = 0
        self.step = 60

        self.json_file = 'model_files/parking_slots.json'  

        my_file = open("model_files/parking_coco.txt", "r")
        data = my_file.read()
        self.class_list = data.split("\n")

        with open("model_files/parking_polygon_coordinates.txt", "r") as my_file:
            data = my_file.read()
            
        # define the class id car, motorcycle, bus, truck
        self.class_IDS = [2, 3, 5, 7]

        self.slot_list = []
        for line in data.split('\n'):
            if line:
                parts = line.split(': ')
                slot_name = parts[0]
                coordinates = eval(parts[1])
                self.slot_list.append(Slot(slot_name, coordinates))
        
        self.px = pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2', 'class'])

        # create a list of random self.colors to represent each class
        np.random.seed(42)  # to get the same self.colors
        self.colors = np.random.randint(0, 255, size=(len(self.class_list), 3))  # (80, 3)
        print("parking model initialized")

    def detect(self, frame):
        ori_frame_height, ori_frame_width, _ = frame.shape

        frame=cv2.resize(frame,(1920,1080))

        count = 0
        if self.frame_nmr % self.step == 0 or count == 0:
            results = self.model.predict(frame, classes = self.class_IDS)

            a=results[0].boxes.xyxy
            classes = results[0].boxes.cls
            self.px=pd.DataFrame(a).astype("float")
            self.px[4] = classes
            count += 1
        self.frame_nmr += 1

        for slot in self.slot_list:
            slot.reset()
        
        for index,row in self.px.iterrows():
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            class_id=int(row[4])

            # get the color associated with the class name
            color = self.colors[class_id]
            B, G, R = int(color[0]), int(color[1]), int(color[2])

            c=self.class_list[class_id]
            cx=int(x1+x2)//2
            cy=int(y1+y2)//2
            
            for slot in self.slot_list:
                availability = cv2.pointPolygonTest(np.array(slot.coordinates,np.int32),((cx,cy)),False)
                if availability>=0:
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(B, G, R),BOX_WEIGHT)
                    cv2.rectangle(frame, (x1 - 1, y1 - 20), (x1 + len(c) * 12, y1), (B, G, R), -1) # box for class name
                    cv2.putText(frame,str(c),(x1+5,y1-8),FONT,0.5,(255,255,255),FONT_WEIGHT)
                    cv2.circle(frame,(cx,cy),CIRCLE_RADIUS,(B, G, R),-1)
                    setattr(slot, 'available', False)
                
        for slot in self.slot_list:
            first_point = [np.array(slot.coordinates, np.int32)][0][0]
            text_position = (first_point[0] + 10, first_point[1] + 15)  # Offset the text position

            if slot.available:
                cv2.polylines(frame, [np.array(slot.coordinates, np.int32)], True, (0, 255, 0), 2)
                cv2.putText(frame,slot.name,text_position,FONT,0.5,(0, 255, 0),FONT_WEIGHT)
                # polygon_points = np.array(slot.coordinates, np.int32)
                # polygon_points = polygon_points.reshape((-1, 1, 2))
                # cv2.fillPoly(frame, [polygon_points], (0, 255, 0))
                # cv2.addWeighted(frame, 0.5, frame, 1 - 0.5, 0, frame)
            else:
                cv2.polylines(frame, [np.array(slot.coordinates, np.int32)], True, (0, 0, 255), 2)
                cv2.putText(frame,slot.name,text_position,FONT,0.5,(0, 0, 255),FONT_WEIGHT)

        available_slots = [slot.name for slot in self.slot_list if slot.available]
        space = ", ".join(available_slots)
        if available_slots:
            cv2.putText(frame, "empty slot: " + str(space),(25,25),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
        else:
            cv2.putText(frame, "No available parking slots.",(25,25),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)

        # Serialize the Slot objects to JSON and write to the file
        with open(self.json_file, "w") as file:
            json.dump([slot.__dict__ for slot in self.slot_list], file, indent=4)
        
        frame=cv2.resize(frame,(ori_frame_width,ori_frame_height))
        return frame