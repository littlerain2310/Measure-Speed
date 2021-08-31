from sort.sort import *
from deep_sort import  nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
class Tracker:
    def __init__(self):
        
        self.tracker = Sort()
    def tracked(self,obj):
        tracked_obj = self.tracker.update(obj)
        return tracked_obj
