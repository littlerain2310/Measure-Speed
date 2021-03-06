from tracker import DeepSort
from detect import ObjectDetection
from trackableobject import TrackableObject
import cv2
import random
from util import bbox_to_centroid
import colorsys
import time
import numpy as np

class MeasureSpeed:
    def __init__(self,input,output = 'result.avi'):
        self.tracker = DeepSort()
        self.detect = ObjectDetection(classes=[0])
        self.input = input
        self.output = output
        self.f_width = 1280
        self.f_height = 720
        self.frame_idx = 0
        self.A_points = 300
        self.B_points = 500
        self.speed = [None] * 1000
        self.video = cv2.VideoCapture(self.input)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.trackableObject = {}
        self.totalFrames =0
        self.objects = []
        self.output_image = None
        
    def get_bb(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,obj = self.detect.get_bb(img)
        return obj
    def calculate_speed(self):
        for (objectID,centroid,color,bbox) in self.objects:
            to = self.trackableObject.get(objectID,None)

            
            if to is None:
                #update position
                to = TrackableObject(objectID,centroid)
            
            elif not to.estimated:   
                to.centroids.append(centroid)   
                
                to.color = color
                # print(to.centroids)
            # check if the direction of the object has been set, if
            # not, calculate it, and set it
                if to.direction is None:
                    to.direction = 0
                if to.direction == 0 and (len(to.centroids) > 2):
                    # print(len(to.centroids))
                    y = [c[1] for c in to.centroids]
                    direction = centroid[1] - np.mean(y)
                    to.direction = direction
                
                #moving forward
                # print(len(to.centroids))
                # print(to.direction)
                if to.direction > 0:
                # check to see if timestamp has been noted for
                # point A
                    if to.timestamp["A"] == 0 :
                        # if the centroid's x-coordinate is greater than
                        # the corresponding point then set the timestamp
                        # as current timestamp and set the position as the
                        # centroid's x-coordinate
                        
                        if centroid[1] > self.A_points:
                            # print('reach A')
                            to.timestamp["A"] = self.frame_idx
                            to.position["A"] = centroid[1]
                    # check to see if timestamp has been noted for
                    # point B
                    elif to.timestamp["B"] == 0:
                        # if the centroid's x-coordinate is greater than
                        # the corresponding point then set the timestamp
                        # as current timestamp and set the position as the
                        # centroid's x-coordinate
                        if centroid[1] > self.B_points:
                            to.timestamp["B"] = self.frame_idx
                            to.position["B"] = centroid[1]
                            # print('reach B')
                            to.lastPoint = True
               
            if to.lastPoint and not to.estimated:
                # print('Estimasting ...')
                # initialize the list of estimated speeds
                estimatedSpeeds = []
                # loop over all the pairs of points and estimate the
                # vehicle speed
                for (i, j) in to.points:
                    # calculate the distance in pixels
                    d = to.position[j] - to.position[i]
                    distanceInPixels = abs(d)

                    number_frame = abs(to.timestamp[j] - to.timestamp[i])
                    # print(distanceInPixels)
                    # check if the distance in pixels is zero, if so,
                    # skip this iteration
                    t = number_frame/int(self.fps)
                    # print(self.fps)
                    if distanceInPixels == 0 or t == 0:
                        continue
                    # calculate the time in hours
                    
                    # calculate distance in kilometers and append the

                    # calculated speed to the list
                    distanceInMeters = distanceInPixels /10
                    meter_per_second = distanceInMeters /t
                    km_per_hour = meter_per_second * 3.6
                    
                    estimatedSpeeds.append(km_per_hour)
                # calculate the average speed
                if len(estimatedSpeeds):
                    to.calculate_speed(estimatedSpeeds)
                # set the object as estimated
                to.estimated = True
                # print("[INFO] Speed of the {} that just passed"\
                #     " is: {:.2f} KMPH".format(to.objectID,to.speedKMPH))
            
                
        # store the trackable object in our dictionary
            to.bbox = bbox
            self.trackableObject[objectID] = to
    def tracking(self,cars,image):
        self.tracker.object = cars
        tracked_cars = self.tracker.tracking(image)
        
        # Thuc hien update position cac car
        for track in tracked_cars.tracks:
            
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()


            #draw on object 
            x1,y1,x2,y2 = [int(x) for x in bbox]
            ID = track.track_id
            random.seed(ID)
            h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
            color = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
            # Calculate centroid from bbox, display it and its unique ID
            centroid = bbox_to_centroid(bbox)
            
            x1,x2,y1,y2 = int(x1),int(x2),int(y1),int(y2)         
            object = (ID,centroid,color,bbox)
            self.objects.append(object)
            to = self.trackableObject.get(ID,None)
            text = "ID {} ".format(ID)
            #estimate speed
            try :
                if to.timestamp['A'] != 0 and to.direction >0:
                    cv2.rectangle(self.output_image, (x1, y1), (x2, y2), color,2)
                    cv2.putText(self.output_image, text, (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                if  to.estimated:

                    text = "ID {} speed : {:.2f}km/h".format(ID,to.speedKMPH)
                    cv2.putText(self.output_image, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            except:
                pass
    def run(self):
        x_shape = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        y_shape = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        start_p1 = (350,self.A_points)
        end_p1 = (752,self.A_points)
        start_p2 = (210,self.B_points)
        end_p2 = (850,self.B_points)
        # out = cv2.VideoWriter(self.output, four_cc, 20, (x_shape, y_shape))
        while True :
            start_time = time.time()
            _, image = self.video.read()

            if image is None:
                break

            image = cv2.resize(image, (self.f_width, self.f_height))
            
            self.output_image = image.copy()
            self.output_image = cv2.line(self.output_image,start_p1,end_p1,(0,255,0),9)
            self.output_image = cv2.line(self.output_image,start_p2,end_p2,(0,255,0),9)
            self.frame_idx += 1
            # Thuc hien detect car trong hinh
            zone_car  = []
            cars = self.get_bb(image)
            for car in cars :
                x1, y1, x2, y2,confidence = car
                if y2 >= self.A_points and x2 <= 850:
                    zone_car.append(car)
            self.tracking(zone_car,image)
            self.calculate_speed()
            

            #calculate fps
            # out.write(self.output_image)
            end_time = time.time()
            cv2.imshow('video', self.output_image)
            # Detect phim Q
            if cv2.waitKey(1) == ord('q'):
                break
a = MeasureSpeed('traffic.mp4')
a.run()