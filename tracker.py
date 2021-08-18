from sort.sort import *

class Tracker:
    def __init__(self):
        
        self.tracker = Sort()
    def tracked(self,obj):
        tracked_obj = self.tracker.update(obj)
        return tracked_obj