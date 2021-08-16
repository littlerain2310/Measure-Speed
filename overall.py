import cv2
import dlib
import math
import time
from util import bbox_to_centroid
from detect  import ObjectDetection
from sort.sort import *
import random
import colorsys
car_detect = ObjectDetection()
video = cv2.VideoCapture('highway.mp4')


# Dinh nghia cac tham so dai , rong
f_width = 640
f_height = 360

# Cai dat tham so : so diem anh / 1 met, o day dang de 1 pixel = 1 met
pixels_per_meter = 1

# Cac tham so phuc vu tracking
frame_idx = 0
car_number = 0
fps = 0


tracked_cars =[]
car_with_IDs =[]

carTracker = {}
carNumbers = {}
carStartPosition = {}
carCurrentPosition = {}
speed = [None] * 1000

# Ham xoa cac tracker khong tot
def remove_bad_tracker():
	global carTracker, carStartPosition, carCurrentPosition

	# Xoa cac car tracking khong tot
	delete_id_list = []

	# Duyet qua cac car
	for car_id in carTracker.keys():
		# Voi cac car ma conf tracking < 4 thi dua vao danh sach xoa
		if carTracker[car_id].update(image) < 4:
			delete_id_list.append(car_id)

	# Thuc hien xoa car
	for car_id in delete_id_list:
		carTracker.pop(car_id, None)
		carStartPosition.pop(car_id, None)
		carCurrentPosition.pop(car_id, None)

	return

# Ham tinh toan toc do
def calculate_speed(startPosition, currentPosition, fps):

	global pixels_per_meter

	# Tinh toan khoang cach di chuyen theo pixel
	distance_in_pixels = math.sqrt(math.pow(currentPosition[0] - startPosition[0], 2) + math.pow(currentPosition[1] - startPosition[1], 2))

	# Tinh toan khoang cach di chuyen bang met
	distance_in_meters = distance_in_pixels / pixels_per_meter

	# Tinh toc do met tren giay
	speed_in_meter_per_second = distance_in_meters * fps
	# Quy doi sang km/h
	speed_in_kilometer_per_hour = speed_in_meter_per_second * 3.6

	return speed_in_kilometer_per_hour

mot_tracker=Sort()
x_shape = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
y_shape = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
four_cc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter('resultsPC.avi', four_cc, 20, (x_shape, y_shape))
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
	_,cars = car_detect.get_bb(gray)
	tracked_cars = mot_tracker.update(cars)
	
	# Thuc hien update position cac car
	for x1,y1,x2,y2,ID in tracked_cars:
		bbox = x1,y1,x2,y2
		random.seed(ID)
		h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
		color = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
		# Calculate centroid from bbox, display it and its unique ID
		centroid = bbox_to_centroid(bbox)
		text = "ID {}".format(ID)
		# cv2.rectangle(output_image, (x1, y1), (x2, y2), color, 4)
		cv2.putText(output_image, text, (centroid[0] - 10, centroid[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
		cv2.circle(output_image, (centroid[0], centroid[1]), 4, color, -1)
	# out.write(output_image)
	# # Tinh toan frame per second
	# end_time = time.time()
	# if not (end_time == start_time):
	# 	fps = 1.0/(end_time - start_time)

	# # Lap qua cac xe da track va tinh toan toc do
	# for i in carStartPosition.keys():
	# 		[x1, y1, w1, h1] = carStartPosition[i]
	# 		[x2, y2, w2, h2] = carCurrentPosition[i]

	# 		carStartPosition[i] = [x2, y2, w2, h2]

	# 		# Neu xe co di chuyen thi
	# 		if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
	# 			# Neu nhu chua tinh toan toc do va toa do hien tai < 200 thi tinh toan toc do
	# 			if (speed[i] is None or speed[i] == 0) and y2<200:
	# 				speed[i] = calculate_speed([x1, y1, w1, h1], [x2, y2, w2, h2],fps)

	# 			# Neu nhu da tinh toc do va xe da vuot qua tung do 200 thi hien thi tong do
	# 			if speed[i] is not None and y2 >= 200:
	# 				cv2.putText(output_image, str(int(speed[i])) + " km/h",
	# 							(x2,  y2),cv2.FONT_HERSHEY_SIMPLEX, 1,
	# 							(0, 255, 255), 2)

	cv2.imshow('video', output_image)
	# Detect phim Q
	if cv2.waitKey(1) == ord('q'):
		break

# cv2.destroyAllWindows()