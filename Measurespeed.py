from sort.sort import *
from detect import ObjectDetection
import cv2
import random
from util import bbox_to_centroid
import colorsys

class MeasureSpeed:
    def __init__(self,input,output = 'result.avi'):
        self.tracker = Sort()
        self.detect = ObjectDetection(classes=[2])
        self.input = input
        self.output = output
        self.f_width = 1280
        self.f_height = 720
        self.frame_idx = 0
        self.video = cv2.VideoCapture(self.input)
        
    def get_bb(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,obj = self.detect.get_bb(img)
        return obj
    def run(self):
        x_shape = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(self.output, four_cc, 20, (x_shape, y_shape))
        while True :
            start_time = time.time()
            _, image = self.video.read()

            if image is None:
                break

            image = cv2.resize(image, (self.f_width, self.f_height))
            output_image = image.copy()

            self.frame_idx += 1
            # remove_bad_tracker()
            
            # Thuc hien detect moi 10 frame
            untrack_cars=[]
            # print('ok')
            
            
            # Thuc hien detect moi 10 frame
            # Thuc hien detect car trong hinh
            
            cars = self.get_bb(image)
            tracked_cars =self.tracker.update(cars)
            
            # Thuc hien update position cac car
            for x1,y1,x2,y2,ID in tracked_cars:
                bbox = x1,y1,x2,y2
                random.seed(ID)
                h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
                color = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
                # Calculate centroid from bbox, display it and its unique ID
                centroid = bbox_to_centroid(bbox)
                text = "ID {} ".format(ID)
                x1,x2,y1,y2 = int(x1),int(x2),int(y1),int(y2)
                # print(a)
                cv2.rectangle(output_image, (x1, y1), (x2, y2), color,2)
                cv2.putText(output_image, text, (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                # cv2.circle(output_image, (centroid[0], centroid[1]), 4, color, -1)
            cv2.imshow('video', output_image)
            # Detect phim Q
            if cv2.waitKey(1) == ord('q'):
                break
a = MeasureSpeed('highway.mp4')
a.run()