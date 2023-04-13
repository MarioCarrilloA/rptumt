import random
import string
import cv2

class Sample():
    def __init__(self, identity="undefined"):
        self.identity = identity
        self.sample_path = "undefined"
        self.total_bboxes = 0
        self.mean = 0.0
        self.sd = 0.0
        self.areas = []
        self.estimated_size = 0.0
        self.image_name = "sample.png"
        self.status = "INVALID"


    def load_sample_image(self):
        img = cv2.imread(self.sample_path + "/" + self.image_name)
        return img

    def load_predicted_image(self):
        img = cv2.imread(self.sample_path + "/prediction/" + self.image_name)
        return img
