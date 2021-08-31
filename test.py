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

dect  = ObjectDetection(classes=[2,3])
nms_max_overlap = 1.0
model_filename = 'model_data/mars-small128.pb'
encoder = gdet.create_box_encoder(model_filename, batch_size=1)
# calculate cosine distance metric
metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.2, 100)
# initialize tracker
tracker = Tracker(metric)

camera = cv2.VideoCapture('traffic.mp4')
while True :
    
    _, image = camera.read()

    if image is None:
        break

    image = cv2.resize(image, (1280,720))
    output_image = image.copy()

    # remove_bad_tracker()

    untrack_cars=[]
    # print('ok')

    detections = []
    scores = []
    # Thuc hien detect car trong hinh
    zone_car  = []
    _,cars = dect.get_bb(image)
    for car in cars :
        x1,y1,x2,y2,confidence = car
        x,y,w,h = xy_xywh(x1,y1,x2,y2)
        detections.append(np.array([x,y,w,h]))
        scores.append(float('%.2f' % confidence))
    detections = np.array(detections)


    features = encoder(image, detections)
    detections = [Detection(bbox, score, feature) for bbox,score, feature in
                    zip(detections,scores, features)]

    # Run non-maxima suppression.
    boxes = np.array([d.tlwh for d in detections])
    scores = np.array([d.confidence for d in detections])
    indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
    detections = [detections[i] for i in indices]
    
    tracker.predict()
    tracker.update(detections)  
    
    for track in tracker.tracks:
        if not track.is_confirmed() or track.time_since_update > 1:
            continue 
        bbox = track.to_tlbr()
        
    # draw bbox on screen
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        color = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        cv2.rectangle(output_image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
        cv2.putText(output_image, str(track.track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)

    # print('ok')
    cv2.imshow('video',output_image)
    # Detect phim Q
    if cv2.waitKey(1) == ord('q'):
        break