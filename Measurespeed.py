from sort.sort import *
from detect import ObjectDetection
from trackableobject import TrackableObject
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
        self.A_points = 100
        self.B_points = 300
        self.fps = 0
        self.speed = [None] * 1000
        self.video = cv2.VideoCapture(self.input)
        self.trackableObject = {}
        self.totalFrames =0
        self.objects = []
        
    def get_bb(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,obj = self.detect.get_bb(img)
        return obj
    def calculate_speed(self):
        for (objectID,centroid) in self.objects:
            to = self.trackableObject.get(objectID,None)

            if to is None:
                #update position
                to = TrackableObject(objectID,centroid)
                
            elif not to.estimated:
            # check if the direction of the object has been set, if
            # not, calculate it, and set it
                if to.direction is None:
                    y = [c[1] for c in to.centroids]
                    direction = centroid[1] - np.mean(y)
                    to.direction = direction
                #moving forward
                # print(to.direction)
                if to.direction >= 0:
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
                #moving backward
                if to.direction < 0:
                    
                    # check to see if timestamp has been noted for
                    # point B
                    if to.timestamp["B"] == 0:
                        # if the centroid's x-coordinate is greater than
                        # the corresponding point then set the timestamp
                        # as current timestamp and set the position as the
                        # centroid's x-coordinate
                        if centroid[1] < self.B_points:
                            to.timestamp["B"] = self.frame_idx
                            to.position["B"] = centroid[1]
                    elif to.timestamp["A"] == 0 :
                        # if the centroid's x-coordinate is greater than
                        # the corresponding point then set the timestamp
                        # as current timestamp and set the position as the
                        # centroid's x-coordinate
                        if centroid[1] < self.A_points:
                            to.timestamp["A"] = self.frame_idx
                            to.position["A"] = centroid[1]
                            to.lastPoint = True
            if to.lastPoint and not to.estimated:
                print('Estimasting ...')
                # initialize the list of estimated speeds
                estimatedSpeeds = []
                # loop over all the pairs of points and estimate the
                # vehicle speed
                for (i, j) in to.points:
                    # calculate the distance in pixels
                    d = to.position[j] - to.position[i]
                    distanceInPixels = abs(d)
                    # check if the distance in pixels is zero, if so,
                    # skip this iteration
                    if distanceInPixels == 0:
                        continue
                    # calculate the time in hours
                    
                    # calculate distance in kilometers and append the
                    
                    # calculated speed to the list
                    distanceInMeters = distanceInPixels * 100
                    distanceInKM = distanceInMeters / 1000
                    estimatedSpeeds.append(distanceInKM * self.fps)
                # calculate the average speed
                to.calculate_speed(estimatedSpeeds)
                # set the object as estimated
                to.estimated = True
                print("[INFO] Speed of the {} that just passed"\
                    " is: {:.2f} MPH".format(to.objectID,to.speedMPH))
        # store the trackable object in our dictionary
        self.trackableObject[objectID] = to
           
    def run(self):
        x_shape = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        y_shape = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        # out = cv2.VideoWriter(self.output, four_cc, 20, (x_shape, y_shape))
        while True :
            start_time = time.time()
            _, image = self.video.read()

            if image is None:
                break

            image = cv2.resize(image, (self.f_width, self.f_height))
            output_image = image.copy()

            self.frame_idx += 1
            # remove_bad_tracker()
            
            untrack_cars=[]
            # print('ok')
            
            
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
                object = (ID,centroid)
                self.objects.append(object)
                self.calculate_speed()
            #calculate fps
            end_time = time.time()
            if not (end_time == start_time):
                self.fps = 1.0/(end_time - start_time)

            cv2.imshow('video', output_image)
            # Detect phim Q
            if cv2.waitKey(1) == ord('q'):
                break
a = MeasureSpeed('highway.mp4')
a.run()