import cv2
import sys
from detect  import ObjectDetection
from util import image_files_from_folder

input_dir = sys.argv[1]
img_files = image_files_from_folder(input_dir)
print('hello')
a = ObjectDetection()

for img_path in img_files:
    Ivehicle = cv2.imread(img_path)
    image,_ = a.get_bb(Ivehicle)
    cv2.imshow('car',image)
    cv2.waitKey(0)
cv2.destroyAllWindows()
