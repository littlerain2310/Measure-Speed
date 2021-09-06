from typing import List
from scipy.optimize.optimize import main
from tracker import DeepSort
from functools import partial
import sys
import cv2
import os
from collections import defaultdict
# from sort.sort import *

def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() ) #different object reference each time
    return list_of_objects



def read_text(filepath):
    with open(filepath, 'r') as file:
        lines = []
        for line in file:
            lines.append(line)
        
    return lines

def get_boxes(filepath):
    gt = read_text(filepath)
    content = [x.strip() for x in gt] 
    box_each_frame = defaultdict(list) #dict has bbox for each frame
    for obj in content:
        l = obj.split(',')
        x,y = int(l[2]),int(l[3])
        x2 = int(l[4]) +x 
        y2 = int(l[5]) +y
        box = [x,y,x2,y2,1]
        box_each_frame[int(l[0])].append(box)
        
    return box_each_frame

input_dir = sys.argv[1]

bb= get_boxes('gt.txt')

tracking = DeepSort()
tracked = []

after_tracked =''#string to be evaluated

for frame in bb:#k is the frame

    image_path = os.path.join(input_dir,f'{frame}.jpg')
    image = cv2.imread(image_path)


    box = bb[frame]
    tracking.object = box
    objects_tracked = tracking.tracking(image)

    for track in objects_tracked.tracks:
        if  track.time_since_update > 1:
                continue 
        bbox = track.to_tlbr()
        x1,y1,x2,y2 = [int(x) for x in bbox]
        x = x1
        y = y1
        width = x2 -x1
        height = y2-y1
        ID = int(track.track_id)
        after_tracked += '{},{},{},{},{},{},{},{},{},{}'.format(frame,ID,x,y,width,height,1,-1,-1,-1)
        after_tracked += '\n'
        # print('{},{},{},{},{},{},{},{},{},{}'.format(frame,ID,x,y,width,height,1,-1,-1,-1))
# print(after_tracked)
with open('dt.txt', 'w') as f:
    f.write('{}'.format(after_tracked))
    f.close()  