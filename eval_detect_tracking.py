from detect import DetectImage
from tracker import DeepSort
import cv2
import sys
from util import image_files_from_folder

input_dir = sys.argv[1]
img_files = image_files_from_folder(input_dir)




det = DetectImage(classes=[2,3,7])
car_track = DeepSort()


detect = ''

#grab last 4 characters of the file name:
def last_4chars(x):
    filename = x.split('/')[-1]
    filename = filename.split('.')[0]
    return(int(filename))

img_files= sorted(img_files, key = last_4chars)   

for img_path in img_files:
    
    filename = img_path.split('/')[-1]
    filename = filename.split('.')[0]
    
    image = cv2.imread(img_path)
    _,bboxes = det.get_bb(img_path)
    car_zone = []
    for box in bboxes: 
        x1,y1,x2,y2,c = box
        if y1 > -0.7*x1 +322 and y1 > 45:
            car_zone.append(box)
    car_track.object = car_zone
    tracked = car_track.tracking(image)
    
    for track in tracked.tracks:
        if not track.is_confirmed() or track.time_since_update > 1:
            continue 
        bbox = track.to_tlbr()
        x1,y1,x2,y2 = bbox
        x = int(x1)
        y = int(y1)
        width = int(x2 -x1)
        height = int(y2-y1)
        ID = int(track.track_id)
        detect += '{},{},{},{},{},{},{},{},{},{}'.format(filename,ID,x,y,width,height,1,-1,-1,-1)
        detect += '\n'
        # print('{},{},{},{},{},{},{},{},{},{}'.format(filename,ID,x,y,width,height,1,-1,-1,-1))
with open('dt_track.txt', 'w') as f:
    f.write('{}'.format(detect))
    f.close()   
