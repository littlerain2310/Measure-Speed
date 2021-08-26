from typing import List
from scipy.optimize.optimize import main
from tracker import Tracker
from functools import partial
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
    box_each_frame = init_list_of_objects(10000)
    for obj in content:
        l = obj.split(',')
        x,y = int(l[2]),int(l[3])
        x2 = int(l[4]) +x 
        y2 = int(l[5]) +y
        box = [x,y,x2,y2,1]
        box_each_frame[int(l[0])-1].append(box)
    return box_each_frame
bb= get_boxes('gt.txt')

tracking = Tracker()
tracked = []
# print(bb[0])
after_tracked =''
# objects_tracked =tracking.update(bb[0])
# objects_tracked =tracking.update(bb[1])
# print(objects_tracked)
for k,box in enumerate(bb):
    objects_tracked =tracking.tracked(box)
    for track in objects_tracked:
        x1,y1,x2,y2,iD = track
        x = int(x1)
        y = int(y1)
        width = int(x2 -x1)
        height = int(y2-y1)
        ID = int(iD)
        after_tracked += '{},{},{},{},{},{},{},{},{},{}'.format(k+1,ID,x,y,width,height,1,-1,-1,-1)
        after_tracked += '\n'
with open('dt.txt', 'w') as f:
    f.write('{}'.format(after_tracked))
    f.close()  