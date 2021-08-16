
import torch
import numpy as np
import cv2
from time import time
import sys


class ObjectDetection:
    """
    The class performs generic object detection on a video file.
    It uses yolo5 pretrained model to make inferences and opencv2 to manage frames.
    Included Features:
    1. Reading and writing of video file using  Opencv2
    2. Using pretrained model to make inferences on frames.
    3. Use the inferences to plot boxes on objects along with labels.
    Upcoming Features:
    """
    def __init__(self, input_file='abc', out_file="Labeled_Video.avi"):
        """
        :param input_file: provide youtube url which will act as input for the model.
        :param out_file: name of a existing file, or a new file in which to write the output.
        :return: void
        """
        self.input_file = input_file
        self.model = self.load_model()
        self.model.conf = 0.4 # set inference threshold at 0.3
        self.model.iou = 0.3 # set inference IOU threshold at 0.3
        self.model.classes = [0] # set model to only detect "Car" class
        self.out_file = out_file
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def get_video_from_file(self):
        """
        Function creates a streaming object to read the video from the file frame by frame.
        :param self:  class object
        :return:  OpenCV object to stream video frame by frame.
        """
        cap = cv2.VideoCapture(self.input_file)
        assert cap is not None
        return cap

    def load_model(self):
        """
        Function loads the yolo5 model from PyTorch Hub.
        """
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def score_frame(self, frame):
        """
        function scores each frame of the video and returns results.
        :param frame: frame to be infered.
        :return: labels and coordinates of objects found.
        """
        self.model.to(self.device)
        results = self.model([frame])
        labels, cord = results.xyxyn[0][:, -1].to('cpu').numpy(), results.xyxyn[0][:, :-1].to('cpu').numpy()
        return labels, cord

    def plot_boxes(self, results, frame):
        """
        plots boxes and labels on frame.
        :param results: inferences made by model
        :param frame: frame on which to  make the plots
        :return: new frame with boxes and labels plotted.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        cars =[]
        for i in range(n):
            row = cord[i]
            x1, y1, x2, y2,confidence = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape),row[4]
            # w = x2-x1
            # h = y2-y1
            car = [x1,y1,x2,y2,confidence]
            cars.append(car)
            bgr = (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 1)
            label = f"{int(row[4]*100)}"
            cv2.putText(frame, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            cv2.putText(frame, f"Total Targets: {n}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame,cars
    def get_bb(self,image):
        results = self.score_frame(image)
        image,cars = self.plot_boxes(results, image)
        return image,cars
    def __call__(self):
        player = self.get_video_from_file() # create streaming service for application
        assert player.isOpened()
        x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        # out = cv2.VideoWriter(self.out_file, four_cc, 20, (x_shape, y_shape))
        fc = 0
        fps = 0
        tfc = int(player.get(cv2.CAP_PROP_FRAME_COUNT))
        tfcc = 0
        while True:
            fc += 1
            start_time = time()
            ret, frame = player.read()
            if not ret:
                break
            
            results = self.score_frame(frame)
            frame,_ = self.plot_boxes(results, frame)
            cv2.imshow('Frame',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            end_time = time()
            fps += 1/np.round(end_time - start_time, 3)
            if fc == 10:
                fps = int(fps / 10)
                tfcc += fc
                fc = 0
                per_com = int(tfcc / tfc * 100)
                print(f"Frames Per Second : {fps} || Percentage Parsed : {per_com}")
            # out.write(frame)
        player.release()


# link = sys.argv[1]
# # output_file = sys.argv[2]
# a = ObjectDetection(link)
# a()