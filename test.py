from pickle import TRUE
import cv2
import torch
from PIL import Image

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model_data/best.pt')  # default

# Images
# for f in ['zidane.jpg', 'bus.jpg']:
#     torch.hub.download_url_to_file('https://ultralytics.com/images/' + f, f)  # download 2 images
# img1 = Image.open('zidane.jpg')  # PIL image
# img2 = cv2.imread('bus.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)
# imgs = [img1, img2]  # batch of images
model.conf = 0.1

model.iou = 0.45
img = cv2.imread('7519.jpg')
# Inference
results = model(img)  # includes NMS

# Results
results.print()  
results.show()  # or .show()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)