import cv2
import sys
from detect  import DetectImage
from util import image_files_from_folder

input_dir = sys.argv[1]
img_files = image_files_from_folder(input_dir)
print(len(img_files))
a = DetectImage(classes=[2,3,7])

for img_path in img_files:
    filename = img_path.split('/')[-1]
    # filename = filename.split('.')[0]
    # image = cv2.imread(filename)
    image,bboxes = a.get_bb(img_path)
    # for b in bboxes:
    #     x1,y1,x2,y2,c = b
    #     cv2.rectangle(image, (x1, y1), (x2, y2), (255,0,0),2)
    cv2.imshow('car',image)
    cv2.waitKey(0)
cv2.destroyAllWindows()


# img = cv2.imread('image000001.jpg')
# cv2.imshow('ok',img)
# cv2.waitKey(0)