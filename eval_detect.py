from detect import DetectImage
from util import image_files_from_folder
import sys

a = DetectImage(classes= [2])

files = sys.argv[1]
img_files = image_files_from_folder(files)

for img_path in img_files:
    filename = img_path.split('/')[-1]
    filename = filename.split('.')[0]
    _,cars = a.get_bb(img_path)
    dt = ''
    for car in cars :
        x1,y1,x2,y2,c = car
        if y1 > -0.7*x1 +322 and y1 > 70:
            dt += 'cars {} {} {} {} {}\n'.format(c,x1,y1,x2,y2)
    with open('eval_detect/{}.txt'.format(filename), 'w') as f:
        f.write('{}'.format(dt))
        f.close()  