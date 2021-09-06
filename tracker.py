from sort.sort import *
from deep_sort import  nn_matching,preprocessing
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from detect import ObjectDetection
import cv2
from util import xy_xywh
import numpy as np
import random
import colorsys
class SortTracker:
    def __init__(self):
        
        self.tracker = Sort()
    def tracked(self,obj):
        tracked_obj = self.tracker.update(obj)
        return tracked_obj
class DeepSort:
    def __init__(self) :
        self.nms_max_overlap = 1.0
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        # calculate cosine distance metric
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.2, 100)
        # initialize tracker
        self.tracker = Tracker(metric)
        self.object = []#object to track
        
    def tracking(self,image):
        prep_obj = []
        scores = []
        self.object = sorted(self.object, key= lambda x : (x[1],x[0]),reverse= True)
        for obj in self.object :
            x1,y1,x2,y2,confidence = obj
            x,y,w,h = xy_xywh(x1,y1,x2,y2)
            prep_obj.append(np.array([x,y,w,h]))
            scores.append(float('%.2f' % confidence))
        prep_obj = np.array(prep_obj)

        features = self.encoder(image, prep_obj)
        prep_obj = [Detection(bbox, score, feature) for bbox,score, feature in
                        zip(prep_obj,scores, features)]

        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in prep_obj])
        scores = np.array([d.confidence for d in prep_obj])
        indices = preprocessing.non_max_suppression(boxes, self.nms_max_overlap, scores)
        prep_obj = [prep_obj[i] for i in indices]
        
        #start tracking
        self.tracker.predict()
        self.tracker.update(prep_obj)
        return self.tracker  
