from detect  import ObjectDetection
from sort.sort import *
import cv2

human_detect = ObjectDetection()
video = cv2.VideoCapture('Venice.mp4')

# Cac tham so phuc vu tracking
frame_idx = 0

mot_tracker = Sort()
# Dinh nghia cac tham so dai , rong
f_width = 640
f_height = 360



def merge_2_elemet(detect,tracker):
    result =[]
    for obj in detect:
        for tracked_oj in tracker:
            if obj[0] == tracked_oj[0]:
                a = concate_2_list(obj,tracked_oj)
                result.append(a)
                break
    return result

def concate_2_list(list1,list2):
    in_first = list1
    in_second = list2

    in_second_but_not_in_first = in_second - in_first

    return list1 + list(in_second_but_not_in_first)

detect_tracker =''
while True:
    start_time = time.time()
    _, image = video.read()

    if image is None:
        break

    image = cv2.resize(image, (f_width, f_height))
    output_image = image.copy()

    frame_idx += 1
    # remove_bad_tracker()

    # Thuc hien detect moi 10 frame
    untrack_cars=[]
    # print('ok')


    # Thuc hien detect moi 10 frame
    # Thuc hien detect car trong hinh
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,human = human_detect.get_bb(gray)
    # print(human)
    try:
        tracked_man = mot_tracker.update(human)
        # print('ok')
    except:
        continue
    confidence = [c[4] for c in human]
    confidence.reverse()
    tracked_with_conf = zip(tracked_man,confidence)
    # Thuc hien update position cac car
    for (x1,y1,x2,y2,ID),confidence in tracked_with_conf:
        # print('ok')
        x1,y1,x2,y2,ID = int(x1),int(y1),int(x2),int(y2),int(ID)
        width = x2 -x1
        height = y2 - y1

        detect_tracker += '{},{},{},{},{},{},{},-1,-1,-1'.format(frame_idx,ID,x1,y2,width,height,confidence)
        detect_tracker += '\n'
   
with open('dt.txt', 'w') as f:
    f.write('{}'.format(detect_tracker))
    f.close()  