from detect import DetectImage
from util import image_files_from_folder


a = DetectImage(classes= [2])

files = '/home/long/Downloads/M-30'
img_files = image_files_from_folder(files)

for img_path in img_files:
    filename = img_path.split('/')[-1]
    filename = filename.split('.')[0]
    _,cars = a.get_bb(img_path)
    dt = ''
    for car in cars :
        x1,y1,x2,y2,c = car
        dt += 'cars {} {} {} {} {}\n'.format(c,x1,y1,x2,y2)
    with open('detect/dt/{}.txt'.format(filename), 'w') as f:
        f.write('{}'.format(dt))
        f.close()  