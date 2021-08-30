from detect import DetectImage
from sort.sort import *
import cv2
import sys
from util import image_files_from_folder

input_dir = sys.argv[1]
img_files = image_files_from_folder(input_dir)




det = DetectImage(classes=[2,3,7])
car_track = Sort()


detect = ''

#grab last 4 characters of the file name:
def last_4chars(x):
    filename = x.split('/')[-1]
    filename = filename.split('.')[0]
    return(filename[5:])

img_files= sorted(img_files, key = last_4chars)   

for img_path in img_files:
    
    filename = img_path.split('/')[-1]
    filename = filename.split('.')[0]
    filenum = filename[5:]
    num = int(filenum)
    new = num -1
    image = cv2.imread(img_path)
    _,bboxes = det.get_bb(img_path)
    car_zone = []
    for box in bboxes: 
        x1,y1,x2,y2,c = box
        if y1 > -0.7*x1 +322 and y1 > 70:
            car_zone.append(box)
    tracked = car_track.update(car_zone)
    
    for track in tracked:
        x1,y1,x2,y2,iD = track
        x = int(x1)
        y = int(y1)
        width = int(x2 -x1)
        height = int(y2-y1)
        ID = int(iD)
        detect += '{},{},{},{},{},{},{},{},{},{}'.format(new,ID,x,y,width,height,1,-1,-1,-1)
        detect += '\n'
with open('dt_track.txt', 'w') as f:
    f.write('{}'.format(detect))
    f.close()   
